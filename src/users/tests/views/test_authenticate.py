import base64
import mock
import pytest
from django.test import Client
from users.views.authenticate import AuthenticateView
from users.views.request_errors import BadRequestError
from users.tests.factories.user_factory import UserFactory


class TestAuthenticateView():

    def test_validate_authorization_header(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'NotAuthorization': ''}
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_basic_mechanism(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'Authorization': 'hmac user:pass'}
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_authorization_formmat(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'Authorization': 'basic userpass'}
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_passing_email_and_pass(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'Authorization': 'basic :pass'}
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_64_encoding(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'Authorization': 'basic email:pass'}
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_valid_request(self):
        view = AuthenticateView()
        request = mock.Mock()
        request.headers = {'Authorization': 'basic bmF2YXJyb19sYXV0YXJvQGhvdG1haWwuY29t:TGF1dGFybzU1'}
        assert view.validate(request) is None

    @pytest.mark.django_db
    def test_run_it_raise_error_not_correct_pass(self):
        view = AuthenticateView()
        request = mock.Mock()
        password = '123123123'
        user = UserFactory(password=password)
        email64 = base64.b64encode(user.email.encode('ascii')).decode('ascii')
        password64 = base64.b64encode('incorrect_pass'.encode('ascii')).decode('ascii')
        request.headers = {'Authorization': 'basic {}:{}'.format(email64, password64)}
        with pytest.raises(BadRequestError):
            assert view.run(request)

    @pytest.mark.django_db
    def test_run_return_jwt(self):
        view = AuthenticateView()
        request = mock.Mock()
        password = '123123123'
        user = UserFactory(password=password)
        email64 = base64.b64encode(user.email.encode('ascii')).decode('ascii')
        password64 = base64.b64encode(password.encode('ascii')).decode('ascii')
        request.headers = {'Authorization': 'basic {}:{}'.format(email64, password64)}
        assert view.run(request).status_code is 200

    def test_run_raise_bad_request_when_incorrect_pass(self):
        pass


class TestAuthenticationViewIntegration():

    @pytest.mark.django_db
    def test_get_jwt(self):
        password = '123123123'
        user = UserFactory(password=password)
        email64 = base64.b64encode(user.email.encode('ascii')).decode('ascii')
        password64 = base64.b64encode(password.encode('ascii')).decode('ascii')
        headers = {'HTTP_AUTHORIZATION': 'basic {}:{}'.format(email64, password64)}
        response = Client().post('/users/authenticate/', content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json()['token'] == user.jwt
