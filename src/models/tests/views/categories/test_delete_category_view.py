import json
import pytest
from django.test import Client
from models.views.category_views.delete_category_view import DeleteCategoryView
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
class TestDeleteCategoryView:

    def test_validate_existing_category(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        category = CategoryFactory()
        view = DeleteCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        view.validate(request, category_id=category.id)

    def test_validate_no_existing_category(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = DeleteCategoryView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        with pytest.raises(NotFoundError):
            view.validate(request, category_id=-1)

    def test_validate_not_valid_content_type(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = DeleteCategoryView()
        request = get_fake_jwt_request(user=user, content_type='not valid ct')
        with pytest.raises(BadRequestError):
            view.validate(request, category_id=category.id)

    def test_validate_not_admin(self):
        category = CategoryFactory()
        view = DeleteCategoryView()
        category = CategoryFactory()
        request = get_fake_jwt_request(body=json.dumps({'name': category.name}))
        with pytest.raises(ForbiddenError):
            view.validate(request, category_id=category.id)

    def test_run_delete_category(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = DeleteCategoryView()
        request = get_fake_jwt_request(user=user)
        response = view.run(request, category_id=category.id)
        assert response.status_code == 200
        assert json.loads(response.content).get('deleted') is True
        assert Category.objects.filter(id=category.id).exists() is False


@pytest.mark.django_db
class TestDeleteCategoryViewIntegration():

    def test_delete_category(self):
        category = CategoryFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().delete(
            '/categories/{}'.format(category.id),
            data=None,
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        assert response.json().get('deleted') is True
        assert Category.objects.filter(id=category.id).exists() is False
