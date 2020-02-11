import base64
import json
import jwt
from infra.request.errors import (
    NotAuthorizedError,
    ForbiddenError,
)
from users.models.user import User


class require_jwt:
    """
    Use this decorator when the view needs a jwt
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function

    def validate(self, request):
        self.validate_authorization_header(request)
        self.view.user_payload = self.validate_jwt(request)

    def __call__(self, request, *args, **kwargs):
        self.validate(request)
        return self.function(self.view, request, *args, **kwargs)

    def __get__(self, view_instance, view_class):
        self.view = view_instance
        return self

    @staticmethod
    def validate_authorization_header(request):
        if not request.headers.get('Authorization'):
            raise NotAuthorizedError('You must pass and Authorization header')
        if not request.headers.get('Authorization')[:6] == 'Bearer':
            raise NotAuthorizedError('You must pass and Authorization bearer')

    @staticmethod
    def validate_jwt(request):
        """
        Validate the jwt on request and return the payload
        """
        header, payload, signature = request.headers.get('Authorization')[7:].split('.')
        user_payload = json.loads(base64.decodestring(payload.encode('utf-8') + b'==='))
        user = User.objects.filter(id=user_payload.get('id'))
        if not user:
            raise NotAuthorizedError('Invalid JWT')
        try:
            User.get_payload_from_jwt('{}.{}.{}'.format(header, payload, signature))
        except jwt.exceptions.PyJWTError:
            raise NotAuthorizedError('Invalid JWT')
        if not User.objects.filter(id=user_payload.get('id')).exists():
            raise NotAuthorizedError('Invalid JWT')
        return user_payload


class optional_jwt(require_jwt):
    def validate(self, request):
        if request.headers.get('Authorization'):
            self.validate_authorization_header(request)
            self.view.user_payload = self.validate_jwt(request)


class require_admin(require_jwt):
    def validate(self, request):
        self.validate_authorization_header(request)
        self.view.user_payload = self.validate_jwt(request)
        if not self.view.user_payload['access_level'] >= User.Type.ADMIN_USER_TYPE:
            raise ForbiddenError()
