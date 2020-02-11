import json
from django.http import JsonResponse
from infra.request.errors import (
    BadRequestError,
    NotFoundError,
)
from infra.views import BaseView
from users.models.user import User
from helpers.view_helpers import require_admin


class UpdateUserView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'lastname': {'type': 'string'},
            'email': {'type': 'string'},
            'access_level': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        self.user = json.loads(request.body)
        if not User.objects.filter(id=user_id).exists():
            raise NotFoundError('user not found')
        if self.user.get('email'):
            self.validate_email(self.user.get('email'))
        if self.user.get('password'):
            self.validate_password(self.user.get('password'))

    @staticmethod
    def validate_email(email):
        if not User.validate_email(email):
            raise BadRequestError('Invalid email field')
        if User.objects.filter(email=email).exists():
            raise BadRequestError('The provided email already exists')

    @staticmethod
    def validate_password(password):
        if not User.validate_password(password):
            raise BadRequestError('Invalid password field')

    def run(self, request, user_id, *args, **kwargs):
        paramters = self.user
        if self.user.get('password'):
            paramters['password'] = User.hash_password(paramters['password'])

        user = User.objects.filter(id=user_id)
        user.update(**paramters)
        return JsonResponse({'user': user[0].serialized})
