import base64
import json
import jwt
from infra.request.errors import BadRequestError
from users.models.user import User


class requirejwt:
    """
    Use this decorator when the view needs a jwt
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function

    def __call__(self, request, *args, **kwargs):
        self.validate_authorization_header(request)
        self.view.user_payload = self.validate_jwt(request)
        return self.function(self.view, request, *args, **kwargs)

    def __get__(self, view_instance, view_class):
        self.view = view_instance
        return self

    @staticmethod
    def validate_authorization_header(request):
        if not request.headers.get('Authorization'):
            raise BadRequestError('You must pass and Authorization header')
        if not request.headers.get('Authorization')[:6] == 'Bearer':
            raise BadRequestError('You must pass and Authorization bearer')

    @staticmethod
    def validate_jwt(request):
        """
        Validate the jwt on request and return the payload
        """
        header, payload, signature = request.headers.get('Authorization')[7:].split('.')
        user_payload = json.loads(base64.decodestring(payload.encode('utf-8') + b'==='))
        user = User.objects.filter(id=user_payload.get('id'))
        if not user:
            raise BadRequestError('Invalid JWT')
        try:
            user[0].get_payload_from_jwt('{}.{}.{}'.format(header, payload, signature))
        except jwt.exceptions.PyJWTError:
            raise BadRequestError('Invalid JWT')
        return user_payload
