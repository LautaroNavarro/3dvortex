import pytest
import json
from django.test import Client
from models.views.category_views.list_categories_view import ListCategoriesView
from helpers.testing_helpers import get_fake_jwt_request
from models.tests.factories.category_factory import CategoryFactory
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestListCategoriesView:

    def test_run_get_category(self):
        category = CategoryFactory()
        view = ListCategoriesView()
        request = get_fake_jwt_request()
        response = view.run(request)
        categories_response = json.loads(response.content)
        assert len(categories_response['categories']) == 1
        assert categories_response['categories'][0]['id'] == category.id
        assert categories_response['categories'][0]['father_category_id'] == category.father_category_id
        assert categories_response['categories'][0]['name'] == category.name


@pytest.mark.django_db
class TestListCategoriesViewViewIntegration:

    def test_list_categories(self):
        user = UserFactory()
        category_one = CategoryFactory()
        category_two = CategoryFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get('/categories/', content_type='application/json', **headers)
        assert response.status_code == 200
        categories_response = json.loads(response.content)
        assert len(categories_response['categories']) == 2
        assert categories_response['categories'][0]['id'] == category_one.id
        assert categories_response['categories'][0]['father_category_id'] == category_one.father_category_id
        assert categories_response['categories'][0]['name'] == category_one.name
        assert categories_response['categories'][1]['id'] == category_two.id
        assert categories_response['categories'][1]['father_category_id'] == category_two.father_category_id
        assert categories_response['categories'][1]['name'] == category_two.name
