import json
import mock
import pytest
from django.test import Client
from users.views.user_views.create import CreateUserView
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import BadRequestError


class TestAuthenticateView():

    def test_validate_name_field_required(self):
        view = CreateUserView()
        request = mock.Mock()
        request.body = json.dumps({'': ''})
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_last_name_field_required(self):
        view = CreateUserView()
        request = mock.Mock()
        request.body = json.dumps({'name': 'Lautaro'})
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_email_field_required(self):
        view = CreateUserView()
        request = mock.Mock()
        request.body = json.dumps({
            'name': 'Lautaro',
            'lastname': 'Navarro',
        })
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_password_field_is_required(self):
        view = CreateUserView()
        request = mock.Mock()
        request.body = json.dumps({
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
        })
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    @pytest.mark.django_db
    def test_valid_existing_email(self):
        UserFactory(email='lautaro@hotmail.com')
        view = CreateUserView()
        request = mock.Mock()
        request.body = json.dumps({
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
            'password': 'aS123!123as',
        })
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    @pytest.mark.django_db
    def test_valid_request(self):
        view = CreateUserView()
        request = mock.Mock()
        request.content_type = 'application/json'
        request.body = json.dumps({
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
            'password': 'aS123!123as',
        })
        assert view.validate(request) is None

    @pytest.mark.django_db
    def test_run_create_new_user(self):
        view = CreateUserView()
        view.user = {
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
            'password': 'aS123!123as',
        }
        assert User.objects.filter(email='lautaro@hotmail.com').exists() is False
        view.run(mock.Mock())
        assert User.objects.filter(email='lautaro@hotmail.com').exists() is True

    @pytest.mark.django_db
    def test_run_response(self):
        view = CreateUserView()
        view.user = {
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
            'password': 'aS123!123as',
        }
        response = view.run(mock.Mock())
        expected_response = bytes(json.dumps(
            {
                "id": User.objects.get(email='lautaro@hotmail.com').id,
                "name": "Lautaro",
                "email": "lautaro@hotmail.com",
                "access_level": 0,
                "status": 1,
            }),
            'utf-8'
        )
        assert response.status_code == 200
        assert response.content == expected_response


class TestAuthenticationViewIntegration():

    @pytest.mark.django_db
    def test_create_user(self):
        user = {
            'name': 'Lautaro',
            'lastname': 'Navarro',
            'email': 'lautaro@hotmail.com',
            'password': 'aS123!123as',
        }
        response = Client().post('/users/', user, content_type='application/json')
        assert response.status_code == 200
        db_user = User.objects.get(email='lautaro@hotmail.com')
        assert db_user.check_password('aS123!123as') is True
        assert db_user.name == 'Lautaro'
        assert db_user.lastname == 'Navarro'
