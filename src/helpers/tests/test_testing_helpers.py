import json
import pytest
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestGetFakeJwtRequest:

    def test_get_fake_jwt_request(self):
        fake_request = get_fake_jwt_request()
        assert fake_request.body is b''
        assert fake_request.content_type == 'application/json'
        assert fake_request.headers.get('Authorization') is not None

    def test_get_fake_jwt_request_passing_parameters(self):
        user = UserFactory()
        body = json.dumps({'some': 'thing'})
        fake_request = get_fake_jwt_request(user, 'application/octet-stream', body=body)
        assert fake_request.body == body
        assert fake_request.content_type == 'application/octet-stream'
        expected_authorization = 'Bearer {}'.format(user.jwt)
        assert fake_request.headers.get('Authorization') == expected_authorization
