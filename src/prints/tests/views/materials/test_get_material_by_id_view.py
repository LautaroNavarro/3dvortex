import pytest
import json
from django.test import Client
from prints.views.material_views.get_material_by_id_view import GetMaterialByIdView
from helpers.testing_helpers import get_fake_jwt_request
from prints.tests.factories.material_factory import MaterialFactory
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import NotFoundError


@pytest.mark.django_db
class TestGetMaterialByIdView:

    def test_validate_existing_material(self):
        material = MaterialFactory()
        view = GetMaterialByIdView()
        request = get_fake_jwt_request()
        view.validate(request, material_id=material.id)

    def test_validate_no_existing_material(self):
        view = GetMaterialByIdView()
        request = get_fake_jwt_request()
        with pytest.raises(NotFoundError):
            view.validate(request, material_id=-1)

    def test_run_get_material(self):
        material = MaterialFactory()
        view = GetMaterialByIdView()
        request = get_fake_jwt_request()
        response = view.run(request, material_id=material.id)
        material_response = json.loads(response.content)
        assert material_response['id'] == material.id
        assert material_response['description'] == material.description
        assert material_response['price_per_kilogram'] == material.price_per_kilogram
        assert material_response['name'] == material.name


@pytest.mark.django_db
class TestGetMaterialByIdViewIntegration:

    def test_get_material_by_id(self):
        user = UserFactory()
        material = MaterialFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/materials/{}'.format(material.id),
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        material_response = json.loads(response.content)
        assert material_response['id'] == material.id
        assert material_response['description'] == material.description
        assert material_response['price_per_kilogram'] == material.price_per_kilogram
        assert material_response['name'] == material.name
