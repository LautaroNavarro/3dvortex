import pytest
import json
from django.test import Client
from models.views.category_views.get_category_by_id_view import GetCategoryByIdView
from helpers.testing_helpers import get_fake_jwt_request
from models.tests.factories.category_factory import CategoryFactory
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import NotFoundError


@pytest.mark.django_db
class TestGetCategoryByIdView:

    def test_validate_existing_category(self):
        category = CategoryFactory()
        view = GetCategoryByIdView()
        request = get_fake_jwt_request()
        view.validate(request, category_id=category.id)

    def test_validate_no_existing_category(self):
        view = GetCategoryByIdView()
        request = get_fake_jwt_request()
        with pytest.raises(NotFoundError):
            view.validate(request, category_id=-1)

    def test_run_get_category(self):
        category = CategoryFactory()
        view = GetCategoryByIdView()
        request = get_fake_jwt_request()
        response = view.run(request, category_id=category.id)
        category_response = json.loads(response.content)
        assert category_response['id'] == category.id
        assert category_response['father_category_id'] == category.father_category_id
        assert category_response['name'] == category.name


@pytest.mark.django_db
class TestGetCategoryByIdViewIntegration:

    def test_get_category_by_id(self):
        user = UserFactory()
        category = CategoryFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/categories/{}'.format(category.id),
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        category_response = json.loads(response.content)
        assert category_response['id'] == category.id
        assert category_response['father_category_id'] == category.father_category_id
        assert category_response['name'] == category.name
