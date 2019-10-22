import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from users.models.user import User


class CreateUserView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'lastname': {'type': 'string'},
            'email': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': ['name', 'lastname', 'email', 'password'],
        'additionalProperties': False,
    }

    required_body = True

    def run(self, request, *args, **kwargs):
        user = User(
            email=self.user.get('email'),
            name=self.user.get('name'),
            lastname=self.user.get('lastname'),
            status=User.Status.CONFIRMED_STATUS.value,
            access_level=User.Type.COMMON_USER_TYPE.value,
        )
        user.set_password(self.user.get('password'))
        user.save()
        return JsonResponse(user.serialized)

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        self.user = json.loads(request.body)
        self.validate_email(self.user.get('email'))
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
