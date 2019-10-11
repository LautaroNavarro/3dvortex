import json
import pytest
from django.test import Client
from models.views.category_views.create_category_view import CreateCategoryView
from models.models.category import Category
from helpers.testing_helpers import get_fake_jwt_request
from infra.request.errors import (
    ForbiddenError,
    BadRequestError,
)
from models.tests.factories.category_factory import CategoryFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User


@pytest.mark.django_db
class TestCreateCategoryView:

    def test_validate_not_valid_content_type(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user=user, content_type='not valid ct')
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_body_is_provided_on_request(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user)
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_name_field_is_provided_on_request(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user, body=json.dumps({'some': 12}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_name_is_string(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'some': 12}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_category_with_the_provided_name_exists(self):
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = CreateCategoryView()
        category = CategoryFactory()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': category.name}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_not_admin(self):
        view = CreateCategoryView()
        category = CategoryFactory()
        request = get_fake_jwt_request(body=json.dumps({'name': category.name}))
        with pytest.raises(ForbiddenError):
            view.validate(request)

    def test_validate_father_id_is_string(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': '12',
            'father_category_id': 'some',
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_father_id_exists(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': '12',
            'father_category_id': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_run_create_and_return_object(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': 'home'}))
        response = view.run(request)
        assert response.status_code == 200
        assert json.loads(response.content).get('name') == 'home'
        assert Category.objects.filter(name='home').exists() is True


@pytest.mark.django_db
class TestCreateCategoryViewIntegration():

    def test_upload_image(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        category = CategoryFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {'name': 'furniture', 'father_category_id': category.id}
        response = Client().post('/categories/', data, content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json().get('name') == 'furniture'
        assert response.json().get('father_category_id') == category.id
