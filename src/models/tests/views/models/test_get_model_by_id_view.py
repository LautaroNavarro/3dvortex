import pytest
import json
from django.test import Client
from models.views.model_views.get_model_by_id_view import GetModelByIdView
from helpers.testing_helpers import get_fake_jwt_request
from models.tests.factories.model_factory import ModelFactory
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import (
    NotFoundError,
    ForbiddenError,
)


@pytest.mark.django_db
class TestGetModelByIdView:

    def test_validate_existing_model(self):
        model = ModelFactory(privacy=Model.Privacy.PUBLIC.value)
        view = GetModelByIdView()
        request = get_fake_jwt_request()
        view.validate(request, model_id=model.id)

    def test_validate_no_existing_model(self):
        view = GetModelByIdView()
        request = get_fake_jwt_request()
        with pytest.raises(NotFoundError):
            view.validate(request, model_id=-1)

    def test_validate_no_permissions(self):
        model = ModelFactory(privacy=Model.Privacy.PRIVATE.value)
        view = GetModelByIdView()
        request = get_fake_jwt_request()
        with pytest.raises(ForbiddenError):
            view.validate(request, model_id=model.id)

    def test_run_get_model(self):
        model = ModelFactory()
        view = GetModelByIdView()
        request = get_fake_jwt_request(user=model.user)
        response = view.run(request, model_id=model.id)
        model_response = json.loads(response.content)
        assert model_response['id'] == model.id
        assert model_response['user'] == model.user.id
        assert model_response['name'] == model.name
        assert model_response['description'] == model.description
        assert model_response['model_media']['id'] == model.model_media.id
        assert model_response['model_media']['url'] == model.model_media.url
        assert model_response['volume'] == model.volume
        assert model_response['image_media']['id'] == model.image_media.id
        assert model_response['image_media']['url'] == model.image_media.url
        assert model_response['privacy'] == model.privacy
        assert model_response['category'] == model.category


@pytest.mark.django_db
class TestGetModelByIdViewIntegration:

    def test_get_model_by_id(self):
        user = UserFactory()
        model = ModelFactory(user=user)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/models/{}'.format(model.id),
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        model_response = json.loads(response.content)
        assert model_response['id'] == model.id
        assert model_response['user'] == model.user.id
        assert model_response['name'] == model.name
        assert model_response['description'] == model.description
        assert model_response['model_media']['id'] == model.model_media.id
        assert model_response['model_media']['url'] == model.model_media.url
        assert model_response['volume'] == model.volume
        assert model_response['image_media']['id'] == model.image_media.id
        assert model_response['image_media']['url'] == model.image_media.url
        assert model_response['privacy'] == model.privacy
        assert model_response['category'] == model.category
