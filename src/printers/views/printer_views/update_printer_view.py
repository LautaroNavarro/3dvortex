import json
from django.http import JsonResponse
from infra.views import BaseView
from infra.request.errors import BadRequestError
from helpers.view_helpers import require_admin
from printers.models.printer import Printer
from addresses.models.address import Address
from prints.models.material import Material


class UpdatePrinterView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'address': {'type': 'integer'},
            'status': {'type': 'integer'},
            'model': {'type': 'string'},
            'max_x': {'type': 'string'},
            'max_y': {'type': 'string'},
            'max_z': {'type': 'string'},
            'material': {
                "anyOf": [
                    {"type": "number"},
                    {"type": "null"}
                ]
            }
        },
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, printer_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if not Printer.objects.filter(id=printer_id).exists():
            raise BadRequestError('Provided printer id does not exists.')
        if body.get('address') and not Address.objects.filter(id=body['address']).exists():
            raise BadRequestError('Provided address id does not exists.')
        if body.get('material') and not Material.objects.filter(id=body['material']).exists():
            raise BadRequestError('Provided material id does not exists.')
        try:
            if 'max_x' in body:
                max_x = int(body['max_x'])
            if 'max_y' in body:
                max_y = int(body['max_y'])
            if 'max_z' in body:
                max_z = int(body['max_z'])
        except Exception:
            raise BadRequestError('Print area is not a number.')
        if 'max_x' in body and max_x <= 0 or 'max_y' in body and max_y <= 0 or 'max_z' in body and max_z <= 0:
            raise BadRequestError('Print area can not be less or equal than 0.')

    def run(self, request, printer_id, *args, **kwargs):
        body = json.loads(request.body)
        if body.get('address'):
            body['address_id'] = body['address']
            del body['address']
        if body.get('material'):
            body['material_id'] = body['material']
            del body['material']
        printer = Printer.objects.filter(id=printer_id)
        printer.update(**body)
        return JsonResponse(printer[0].serialized)
