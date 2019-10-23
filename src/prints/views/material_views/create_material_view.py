import re
import json
from infra.views import BaseView
from helpers.view_helpers import require_admin
from infra.request.errors import BadRequestError
from prints.models.material import Material
from django.http import JsonResponse


class CreateMaterialView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'price_per_kilogram': {'type': 'string'}
        },
        'required': ['name', 'price_per_kilogram'],
        'additionalProperties': False,
    }

    required_body = True

    @staticmethod
    def validate_price_string_format(price_string):
        valid_price = re.search('^[0-9]+\.[0-9]{2}$', price_string)
        if not valid_price:
            raise BadRequestError('Price format should be formatted \'22.22\'')

    @staticmethod
    def validate_not_existing_material_name(material_name):
        if Material.objects.filter(name=material_name).exists():
            raise BadRequestError('A material with the provided name already exists')

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        self.validate_price_string_format(body['price_per_kilogram'])
        self.validate_not_existing_material_name(body['name'])

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        material = Material.objects.create(
            name=body['name'],
            price_per_kilogram=body['price_per_kilogram'],
            description=body.get('description', '')
        )
        return JsonResponse(material.serialized)
