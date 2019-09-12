import mock
import pytest
from users.views.authenticate import AuthenticateView
from users.views.request_errors import BadRequestError


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
