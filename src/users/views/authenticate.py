from django.http import JsonResponse
from django.views import View
from users.views.request_errors import BadRequestError
from users.views.request_error_handler import request_error_handler
from users.models.user import User
import base64


class AuthenticateView(View):

    def validate_basic_mechanism(self, authorization_header):
        if authorization_header[:5] == 'basic':
            return True
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

    @request_error_handler
    def post(self, request):
        self.validate(request)

        email, password = request.headers['Authorization'][6:].split(':')
        user = User.objects.filter(email=base64.b64decode(email.encode('ascii')).decode())
        if not user:
            raise BadRequestError('Invalid user or password')
        if user[0].check_password(base64.b64decode(password.encode('ascii')).decode()):
            return JsonResponse({'token': user[0].jwt})
        raise BadRequestError('Invalid user or password')
