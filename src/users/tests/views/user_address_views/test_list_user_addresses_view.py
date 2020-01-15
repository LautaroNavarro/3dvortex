import json
import pytest
from django.test import Client
from users.views.address_views.list_user_addresses_view import ListUserAddressesView
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import (
    BadRequestError,
    NotAuthorizedError,
)
from helpers.testing_helpers import get_fake_jwt_request
from addresses.models.address import Address
from addresses.tests.factories.address_factory import AddressFactory


@pytest.mark.django_db
class TestListUserAddressesView():

    def test_validate_no_authorized(self):
        view = ListUserAddressesView()
        request = get_fake_jwt_request(body=json.dumps({
            'name': 'My house',
            'latitude': '123123',
            'longitude': '123123',
        }))
        with pytest.raises(NotAuthorizedError):
            assert view.validate(request, -1)

    def test_validate_valid_request(self):
        view = ListUserAddressesView()
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

    def test_run_returns_list_of_addresses(self):
        user = UserFactory()
        address = AddressFactory()
        user.addresses.add(address)
        request = get_fake_jwt_request(
            user=user,
            body=json.dumps({
                'name': 'My house',
                'latitude': '123123',
                'longitude': '123123',
            })
        )
        view = ListUserAddressesView()
        view.user_payload = user.serialized
        response = view.run(request, 1, user.id)
        response_body = json.loads(response.content)
        assert len(response_body['addresses']) == 1
        assert response_body['addresses'][0]['id'] == address.id
        assert response_body['addresses'][0]['name'] == address.name
        assert response_body['addresses'][0]['latitude'] == address.latitude
        assert response_body['addresses'][0]['longitude'] == address.longitude


@pytest.mark.django_db
class TestCreateUserAddressViewIntegration():

    def test_list_user_address(self):
        user = UserFactory()
        address = AddressFactory()
        user.addresses.add(address)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/users/{}/addresses'.format(user.id),
            **headers
        )
        assert response.status_code == 200
        assert len(response.json()['addresses']) == 1
        assert response.json()['addresses'][0]['id'] == address.id
        assert response.json()['addresses'][0]['name'] == address.name
        assert response.json()['addresses'][0]['latitude'] == address.latitude
        assert response.json()['addresses'][0]['longitude'] == address.longitude
