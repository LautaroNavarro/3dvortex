import pytest
import mock
import jwt
from helpers.view_helpers import (
    require_admin,
    require_jwt,
)
from infra.request.errors import (
    NotAuthorizedError,
    ForbiddenError,
)
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory
from users.models.user import User


class TestingRequireJwtDecorator:

    class TestView:
        @require_jwt
        def validate(self, request):
            return self.user_payload

    def test_not_authorization_header(self):
        request = mock.Mock()
        request.headers.get.return_value = None
        view = self.TestView()
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request)

    def test_not_bearer_authorization_token(self):
        request = mock.Mock()
        request.headers.get.return_value = 'Basic user:password'
        view = self.TestView()
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request)

    @pytest.mark.django_db
    @mock.patch('helpers.view_helpers.User.objects.filter')
    def test_not_user_belong_to_jwt(self, mock_user_manager_filter):
        mock_user_manager_filter.return_value = []
        request = get_fake_jwt_request()
        view = self.TestView()
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request)

    @pytest.mark.django_db
    @mock.patch('helpers.view_helpers.User.get_payload_from_jwt')
    def test_corrupted_jwt(self, get_payload_from_jwt_mock):
        get_payload_from_jwt_mock.side_effect = jwt.exceptions.PyJWTError()
        request = get_fake_jwt_request()
        view = self.TestView()
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request)

    @pytest.mark.django_db
    def test_setting_payload_correctly(self):
        user = UserFactory()
        request = get_fake_jwt_request(user)
        view = self.TestView()
        payload = view.validate(request)
        assert payload == user.get_payload_from_jwt(user.jwt)


@pytest.mark.django_db
class TestingRequireAdminDecorator:

    class TestView:
        @require_admin
        def validate(self, request):
            return self.user_payload

    def test_not_admin(self):
        user = UserFactory()
        request = get_fake_jwt_request(user)
        view = self.TestView()
        with pytest.raises(ForbiddenError):
            assert view.validate(request)

    def test_admin_user(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE.value)
        request = get_fake_jwt_request(user)
        view = self.TestView()
        payload = view.validate(request)
        assert payload == user.get_payload_from_jwt(user.jwt)

    def test_printer_user(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE.value)
        request = get_fake_jwt_request(user)
        view = self.TestView()
        payload = view.validate(request)
        assert payload == user.get_payload_from_jwt(user.jwt)
