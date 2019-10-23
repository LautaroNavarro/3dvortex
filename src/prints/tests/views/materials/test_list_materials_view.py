import pytest
import json
from django.test import Client
from prints.views.material_views.list_materials_view import ListMaterialsView
from helpers.testing_helpers import get_fake_jwt_request
from prints.tests.factories.material_factory import MaterialFactory
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestListMaterialsView:

    def test_run_get_materials(self):
        category = MaterialFactory()
        view = ListMaterialsView()
        request = get_fake_jwt_request()
        response = view.run(request)
        materials_response = json.loads(response.content)
        assert len(materials_response['materials']) == 1
        assert materials_response['materials'][0]['id'] == category.id
        assert materials_response['materials'][0]['name'] == category.name
        assert materials_response['materials'][0]['description'] == category.description
        assert materials_response['materials'][0]['price_per_kilogram'] == category.price_per_kilogram


@pytest.mark.django_db
class TestListMaterialsViewViewIntegration:

    def test_list_categories(self):
        user = UserFactory()
        category_one = MaterialFactory()
        category_two = MaterialFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get('/materials/', content_type='application/json', **headers)
        assert response.status_code == 200
        materials_response = json.loads(response.content)
        assert len(materials_response['materials']) == 2
        assert materials_response['materials'][0]['id'] == category_one.id
        assert materials_response['materials'][0]['name'] == category_one.name
        assert materials_response['materials'][0]['description'] == category_one.description
        assert materials_response['materials'][0]['price_per_kilogram'] == category_one.price_per_kilogram
        assert materials_response['materials'][1]['id'] == category_two.id
        assert materials_response['materials'][1]['name'] == category_two.name
        assert materials_response['materials'][1]['description'] == category_two.description
        assert materials_response['materials'][1]['price_per_kilogram'] == category_two.price_per_kilogram
