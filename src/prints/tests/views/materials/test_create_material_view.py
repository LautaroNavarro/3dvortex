import json
import pytest
from django.test import Client
from prints.views.material_views.create_material_view import CreateMaterialView
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from helpers.testing_helpers import get_fake_jwt_request
from infra.request.errors import BadRequestError
from prints.models.material import Material
from prints.tests.factories.material_factory import MaterialFactory


class TestCreateMaterialView:

    def test_validate_price_string_format_invalid_formats(self):
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('10.1')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('10.1s')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('10,s1')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('10')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('asd')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('10.')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_price_string_format('.10')

    def test_validate_price_string_format_valid_format(self):
        CreateMaterialView.validate_price_string_format('10.10')

    @pytest.mark.django_db
    def test_validate_not_existing_material_name_invalid_name(self):
        MaterialFactory(name='existing name')
        with pytest.raises(BadRequestError):
            CreateMaterialView.validate_not_existing_material_name('existing name')

    @pytest.mark.django_db
    def test_validate_not_existing_material_name_valid_name(self):
        CreateMaterialView.validate_not_existing_material_name('not existing name')

    @pytest.mark.django_db
    def test_validate_name_is_required_in_schema(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = CreateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'price_per_kilogram': '12.00'}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    @pytest.mark.django_db
    def test_validate_price_per_kilogram_is_required_in_schema(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = CreateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': 'some'}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    @pytest.mark.django_db
    def test_validate_valid_request(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = CreateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': 'some',
            'price_per_kilogram': '12.00',
        }))
        view.validate(request)

    @pytest.mark.django_db
    def test_run_creates_new_material(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': 'some',
            'price_per_kilogram': '12.00',
            'description': 'Some description'
        }))
        view.run(request)
        assert Material.objects.filter(name='some').exists() is True


class TestCreateMaterialViewIntegration:

    @pytest.mark.django_db
    def test_create_material(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {
            'name': 'some',
            'price_per_kilogram': '12.00',
            'description': 'Some description'
        }
        response = Client().post('/materials/', data, content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json()['name'] == 'some'
        assert response.json()['price_per_kilogram'] == '12.00'
        assert response.json()['description'] == 'Some description'
