from users.tests.factories.user_factory import UserFactory
import mock


def get_fake_jwt_request(user=None, content_type='application/json', body=None):
    if not user:
        user = UserFactory()
    request = mock.Mock()
    request.content_type = content_type
    request.body = body
    request.headers = {
        'Content-Type': content_type,
        'Authorization': 'Bearer {}'.format(user.jwt)
    }
    return request