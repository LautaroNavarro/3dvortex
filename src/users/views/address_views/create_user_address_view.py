import json
from django.http import JsonResponse
from infra.views import BaseView
from infra.request.errors import NotAuthorizedError
from users.models.user import User
from addresses.models.address import Address
from helpers.view_helpers import require_jwt


class CreateUserAddressView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'latitude': {'type': 'string'},
            'longitude': {'type': 'string'},
        },
        'required': ['name', 'latitude', 'longitude'],
        'additionalProperties': False,
    }

    required_body = True

    @require_jwt
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if self.user_payload['id'] != user_id:
            raise NotAuthorizedError('You are not allow to create addresses for this user')

    def run(self, request, user_id, *args, **kwargs):
        address_dict = json.loads(request.body)
        address = Address.objects.create(
            name=address_dict.get('name'),
            latitude=address_dict.get('latitude'),
            longitude=address_dict.get('longitude'),
        )
        user = User.objects.get(id=self.user_payload['id'])
        user.addresses.add(address)
        return JsonResponse(address.serialized)
