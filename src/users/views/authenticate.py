from django.http import JsonResponse
from django.views import View
from users.views.request_errors import BadRequestError
from users.views.request_error_handler import RequestErrorHandler


class AuthenticateView(View):

    def validate_hmac_mechanism(self, authorization_header):
        if authorization_header[:4] == 'hmac':
            return True
        return False

    def validate(self, request):
        if not self.validate_hmac_mechanism(request.headers['Authorization']):
            raise BadRequestError('Authorization must be hmac')
        user_and_password = request.headers['Authorization'][5:].split(':')
        if len(user_and_password) != 2:
            raise BadRequestError('Bad header format')
        if not (user_and_password[0] and user_and_password[1]):
            raise BadRequestError('You must provide user:password')

    def post(self, request):
        errors = RequestErrorHandler(lambda: self.validate(request))
        if errors:
            return errors

        return JsonResponse({'response': True})
