import pytest
import mock
import jwt
from helpers.view_helpers import requirejwt
from infra.request.errors import BadRequestError
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


class TestingRequireJwtDecorator:

    class TestView:
        @requirejwt
        def validate(self, request):
            return self.user_payload

    def test_not_authorization_header(self):
        request = mock.Mock()
        request.headers.get.return_value = None
        view = self.TestView()
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_not_bearer_authorization_token(self):
        request = mock.Mock()
        request.headers.get.return_value = 'Basic user:password'
        view = self.TestView()
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    @pytest.mark.django_db
    @mock.patch('helpers.view_helpers.User.objects.filter')
    def test_not_user_belong_to_jwt(self, mock_user_manager_filter):
        mock_user_manager_filter.return_value = []
        request = get_fake_jwt_request()
        view = self.TestView()
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    @pytest.mark.django_db
    @mock.patch('helpers.view_helpers.User.get_payload_from_jwt')
    def test_corrupted_jwt(self, get_payload_from_jwt_mock):
        get_payload_from_jwt_mock.side_effect = jwt.exceptions.PyJWTError()
        request = get_fake_jwt_request()
        view = self.TestView()
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    @pytest.mark.django_db
    def test_setting_payload_correctly(self):
        user = UserFactory()
        request = get_fake_jwt_request(user)
        view = self.TestView()
        payload = view.validate(request)
        assert payload == user.get_payload_from_jwt(user.jwt)
