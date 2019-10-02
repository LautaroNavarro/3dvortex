import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from users.models.user import User


class CreateUserView(BaseView):

    def run(self, request):
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

    def validate(self, request):
        self.user = json.loads(request.body)
        if not self.user.get('name'):
            raise BadRequestError('name field is mandatory')
        if not self.user.get('lastname'):
            raise BadRequestError('lastname field is mandatory')
        if not self.user.get('email'):
            raise BadRequestError('email field is mandatory')
        if not self.user.get('password'):
            raise BadRequestError('password field is mandatory')
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
