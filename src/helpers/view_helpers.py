import base64
import json
import jwt
from infra.request.errors import BadRequestError
from users.models.user import User


def requirejwt(validate):
    """
    Use this decorator when the view needs a jwt
    """
    def wrapper(view, request, *args, **kwargs):
        if not request.headers.get('Authorization'):
            raise BadRequestError('You must pass and Authorization header')
        if not request.headers.get('Authorization')[:6] == 'Bearer':
            raise BadRequestError('You must pass and Authorization bearer')
        header, payload, signature = request.headers.get('Authorization')[7:].split('.')
        user_payload = json.loads(base64.decodestring(payload.encode('utf-8') + b'==='))
        user = User.objects.filter(id=user_payload.get('id'))
        if not user:
            raise BadRequestError('Invalid JWT')
        try:
            user[0].get_payload_from_jwt('{}.{}.{}'.format(header, payload, signature))
        except jwt.exceptions.PyJWTError:
            raise BadRequestError('Invalid JWT')
        view.user_payload = user_payload
        return validate(view, request, *args, **kwargs)
    return wrapper
