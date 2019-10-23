import json
import pytest
from django.test import Client
from prints.views.material_views.delete_material_view import DeleteMaterialView
from prints.models.material import Material
from helpers.testing_helpers import get_fake_jwt_request
from infra.request.errors import (
    ForbiddenError,
    NotFoundError,
)
from prints.tests.factories.material_factory import MaterialFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User


@pytest.mark.django_db
class TestDeleteMaterialView:

    def test_validate_existing_material(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        material = MaterialFactory()
        view = DeleteMaterialView()
        request = get_fake_jwt_request(user=user, body=json.dumps({}))
        view.validate(request, material_id=material.id)

    def test_validate_no_existing_material(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = DeleteMaterialView()
        request = get_fake_jwt_request(user=user)
        with pytest.raises(NotFoundError):
            view.validate(request, material_id=-1)

    def test_validate_not_admin(self):
        material = MaterialFactory()
        view = DeleteMaterialView()
        material = MaterialFactory()
        request = get_fake_jwt_request()
        with pytest.raises(ForbiddenError):
            view.validate(request, material_id=material.id)

    def test_run_delete_material(self):
        material = MaterialFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = DeleteMaterialView()
        request = get_fake_jwt_request(user=user)
        response = view.run(request, material_id=material.id)
        assert response.status_code == 200
        assert json.loads(response.content).get('deleted') is True
        assert Material.objects.filter(id=material.id).exists() is False


@pytest.mark.django_db
class TestDeleteMaterialViewIntegration():

    def test_delete_material(self):
        material = MaterialFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().delete(
            '/materials/{}'.format(material.id),
            data=None,
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        assert response.json().get('deleted') is True
        assert Material.objects.filter(id=material.id).exists() is False
