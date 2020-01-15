import json
import pytest
from django.test import Client
from users.views.address_views.create_user_address_view import CreateUserAddressView
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import (
    BadRequestError,
    NotAuthorizedError,
)
from helpers.testing_helpers import get_fake_jwt_request
from addresses.models.address import Address


@pytest.mark.django_db
class TestCreateUserAddressView():

    def test_validate_name_field_is_required(self):
        view = CreateUserAddressView()
        request = get_fake_jwt_request(body=json.dumps({'': ''}))
        with pytest.raises(BadRequestError):
            assert view.validate(request, 1)

    def test_validate_latitude_field_is_required(self):
        view = CreateUserAddressView()
        request = get_fake_jwt_request(body=json.dumps({'name': 'My house'}))
        with pytest.raises(BadRequestError):
            assert view.validate(request, 1)

    def test_validate_longitude_field_is_required(self):
        view = CreateUserAddressView()
        request = get_fake_jwt_request(body=json.dumps({
            'name': 'My house',
            'latitude': '123123',
        }))
        with pytest.raises(BadRequestError):
            assert view.validate(request, 1)

    def test_validate_no_authorized_field_is_required(self):
        view = CreateUserAddressView()
        request = get_fake_jwt_request(body=json.dumps({
            'name': 'My house',
            'latitude': '123123',
            'longitude': '123123',
        }))
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request, -1)

    def test_validate_valid_request(self):
        view = CreateUserAddressView()
        user = UserFactory()
        request = get_fake_jwt_request(
            user=user,
            body=json.dumps({
                'name': 'My house',
                'latitude': '123123',
                'longitude': '123123',
            })
        )
        view.validate(request, user.id)

    def test_run_create_and_return_object(self):
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        view = CreateUserAddressView()
        view.user_payload = user.serialized
        request = get_fake_jwt_request(user, body=json.dumps({
            'name': 'My house',
            'latitude': '123123',
            'longitude': '123123',
        }))
        response = view.run(request, user.id)
        assert response.status_code == 200
        response_body = json.loads(response.content)
        assert response_body['name'] == 'My house'
        assert response_body['latitude'] == '123123'
        assert response_body['longitude'] == '123123'
        assert Address.objects.filter(id=response_body['id']).exists() is True


@pytest.mark.django_db
class TestCreateUserAddressViewIntegration():

    def test_create_user_address(self):
        user = UserFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {
            'name': 'My house',
            'latitude': '123123',
            'longitude': '123123',
        }
        response = Client().post(
            '/users/{}/addresses'.format(user.id),
            data,
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        assert response.json()['name'] == 'My house'
        assert response.json()['latitude'] == '123123'
        assert response.json()['longitude'] == '123123'
