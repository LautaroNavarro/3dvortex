import mock
import json
import pytest
from django.test import Client
from prints.views.material_views.update_material_view import UpdateMaterialView
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from helpers.testing_helpers import get_fake_jwt_request
from infra.request.errors import BadRequestError
from prints.models.material import Material
from prints.tests.factories.material_factory import MaterialFactory


class TestUpdateMaterialView:

    def test_validate_price_string_format_invalid_formats(self):
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('10.1')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('10.1s')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('10,s1')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('10')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('asd')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('10.')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_price_string_format('.10')

    def test_validate_price_string_format_valid_format(self):
        UpdateMaterialView.validate_price_string_format('10.10')

    @pytest.mark.django_db
    def test_validate_not_existing_material_name_invalid_name(self):
        MaterialFactory(name='existing name')
        with pytest.raises(BadRequestError):
            UpdateMaterialView.validate_not_existing_material_name('existing name')

    @pytest.mark.django_db
    def test_validate_not_existing_material_name_valid_name(self):
        UpdateMaterialView.validate_not_existing_material_name('not existing name')

    @pytest.mark.django_db
    @mock.patch(
        'prints.views.material_views.update_material_view.UpdateMaterialView.validate_price_string_format'
    )
    def test_validate_price_is_not_called_if_not_price_in_request(self, validate_price_mock):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        view.validate(request, material_id=1)
        assert validate_price_mock.called is False

    @pytest.mark.django_db
    @mock.patch(
        'prints.views.material_views.update_material_view.UpdateMaterialView.validate_price_string_format'
    )
    def test_validate_price_is_called_if_price_in_request(self, validate_price_mock):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'price_per_kilogram': '12.00'}))
        view.validate(request, material_id=1)
        assert validate_price_mock.called is True

    @pytest.mark.django_db
    @mock.patch(
        'prints.views.material_views.update_material_view.UpdateMaterialView.validate_not_existing_material_name'
    )
    def test_validate_name_is_not_called_if_not_name_in_request(self, validate_name):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        view.validate(request, material_id=1)
        assert validate_name.called is False

    @pytest.mark.django_db
    @mock.patch(
        'prints.views.material_views.update_material_view.UpdateMaterialView.validate_not_existing_material_name'
    )
    def test_validate_name_is_called_if_name_in_request(self, validate_name):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': 'some name'}))
        view.validate(request, material_id=1)
        assert validate_name.called is True

    @pytest.mark.django_db
    def test_validate_valid_request(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': 'some',
            'price_per_kilogram': '12.00',
        }))
        view.validate(request, material_id=1)

    @pytest.mark.django_db
    def test_run_creates_new_material(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateMaterialView()
        material = MaterialFactory()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': 'some',
            'price_per_kilogram': '12.00',
            'description': 'Some description'
        }))
        view.run(request, material_id=material.id)
        material = Material.objects.get(id=material.id)
        assert material.name == 'some'
        assert material.price_per_kilogram == '12.00'
        assert material.description == 'Some description'


class TestUpdateMaterialViewIntegration:

    @pytest.mark.django_db
    def test_update_material(self):
        material = MaterialFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {
            'name': 'some',
            'price_per_kilogram': '12.00',
            'description': 'Some description'
        }
        response = Client().put(
            '/materials/{}'.format(material.id),
            data,
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        assert response.json()['name'] == 'some'
        assert response.json()['price_per_kilogram'] == '12.00'
        assert response.json()['description'] == 'Some description'
