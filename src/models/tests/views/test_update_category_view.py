import json
import pytest
from django.test import Client
from models.views.category_views.update_category_view import UpdateCategoryView
from models.models.category import Category
from helpers.testing_helpers import get_fake_jwt_request
from infra.request.errors import (
    ForbiddenError,
    BadRequestError,
    NotFoundError,
)
from models.tests.factories.category_factory import CategoryFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User


@pytest.mark.django_db
class TestUpdateCategoryView:

    def test_validate_existing_category(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        category = CategoryFactory()
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        view.validate(request, category_id=category.id)

    def test_validate_no_existing_category(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        with pytest.raises(NotFoundError):
            view.validate(request, category_id=-1)

    def test_validate_not_valid_content_type(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, content_type='not valid ct')
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_body_is_provided_on_request(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user)
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_name_is_string(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': 12}))
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_category_with_the_provided_name_exists(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.PRINTER_USER_TYPE)
        view = UpdateCategoryView()
        category = CategoryFactory()
        request = get_fake_jwt_request(user=user, body=json.dumps({'name': category.name}))
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_not_admin(self):
        category = CategoryFactory()
        view = UpdateCategoryView()
        category = CategoryFactory()
        request = get_fake_jwt_request(body=json.dumps({'name': category.name}))
        with pytest.raises(ForbiddenError):
            view.validate(request, category_id=category.id)

    def test_validate_father_id_is_string(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': '12',
            'father_category_id': 'some',
        }))
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_father_id_exists(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': '12',
            'father_category_id': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_run_update_category(self):
        father_category = CategoryFactory()
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = UpdateCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({
            'name': 'home',
            'father_category_id': father_category.id,
        }))
        response = view.run(request, category_id=category.id)
        assert response.status_code == 200
        assert json.loads(response.content).get('name') == 'home'
        assert json.loads(response.content).get('father_category_id') == father_category.id
        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == 'home'
        assert updated_category.father_category_id == father_category.id


@pytest.mark.django_db
class TestUpdateCategoryViewIntegration():

    def test_upload_image(self):
        father_category = CategoryFactory()
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {'name': 'furniture', 'father_category_id': father_category.id}
        response = Client().put('/categories/{}'.format(category.id), data, content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json().get('name') == 'furniture'
        assert response.json().get('father_category_id') == father_category.id
        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == 'furniture'
        assert updated_category.father_category_id == father_category.id
