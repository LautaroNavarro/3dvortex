import json
from django.http import JsonResponse
from infra.views import BaseView
from infra.request.errors import BadRequestError
from helpers.view_helpers import require_admin
from printers.models.printer import Printer
from addresses.models.address import Address


class CreatePrinterView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'address': {'type': 'integer'},
            'model': {'type': 'string'},
            'max_x': {'type': 'string'},
            'max_y': {'type': 'string'},
            'max_z': {'type': 'string'},
        },
        'required': ['name', 'address', 'max_x', 'max_y', 'max_z'],
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if not Address.objects.filter(id=body['address']).exists():
            raise BadRequestError('Provided address id does not exists.')
        if not body['max_x'] or not body['max_y'] or not body['max_z']:
            raise BadRequestError('Empty print area')
        try:
            max_x = int(body['max_x'])
            max_y = int(body['max_y'])
            max_z = int(body['max_z'])
        except Exception:
            raise BadRequestError('Print area is not a number.')
        if max_x <= 0 or max_y <= 0 or max_z <= 0:
            raise BadRequestError('Print area can not be less or equal than 0.')

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        body['address_id'] = body['address']
        del body['address']
        printer = Printer(**body)
        printer.save()
        return JsonResponse(printer.serialized)
