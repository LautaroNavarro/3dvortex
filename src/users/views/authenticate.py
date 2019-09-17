from django.http import JsonResponse
from django.views import View
from infra.request.errors import BadRequestError
from infra.views import BaseView
from users.models.user import User
import base64


class AuthenticateResourceView(View):

    def post(self, request):
        view = AuthenticateView()
        return view(request)


class AuthenticateView(BaseView):

    def validate_basic_mechanism(self, authorization_header):
        if authorization_header[:5] == 'basic':
            return True
        return False

    def valid_64_encoding(self, string):
        try:
            base64.b64decode(string.encode('ascii')).decode('ascii')
            return True
        except Exception:
            return False

    def validate(self, request):
        if not request.headers.get('Authorization'):
            raise BadRequestError('You must provide an Authorization header.')
        if not self.validate_basic_mechanism(request.headers['Authorization']):
            raise BadRequestError('Authorization header must be basic.')
        user_and_password = request.headers['Authorization'][6:].split(':')
        if len(user_and_password) != 2:
            raise BadRequestError('Bad Authorization header format.')
        if not (user_and_password[0] and user_and_password[1]):
            raise BadRequestError('You must provide email:password on Authorization.')
        if not (self.valid_64_encoding(user_and_password[0]) and self.valid_64_encoding(user_and_password[1])):
            raise BadRequestError('Invalid 64 encoding.')

    def run(self, request):
        email, password = request.headers['Authorization'][6:].split(':')
        user = User.objects.filter(email=base64.b64decode(email.encode('ascii')).decode('ascii'))
        if not user:
            raise BadRequestError('Invalid user or password')
        if user[0].check_password(base64.b64decode(password.encode('ascii')).decode('ascii')):
            return JsonResponse({'token': user[0].jwt})
        raise BadRequestError('Invalid user or password')
