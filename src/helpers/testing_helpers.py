import mock
from users.tests.factories.user_factory import UserFactory


def get_fake_jwt_request(user=None, content_type='application/json', body=b''):
    if not user:
        user = UserFactory()
    request = mock.Mock()
    request.content_type = content_type
    request.body = body
    if body:
        request.body = body
    request.headers = {
        'Content-Type': content_type,
        'Authorization': 'Bearer {}'.format(user.jwt)
    }
    return request
