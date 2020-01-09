import pytest
import json
from django.test import Client
from models.views.model_views.list_models_view import ListModelsView
from helpers.testing_helpers import get_fake_jwt_request
from models.tests.factories.model_factory import ModelFactory
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestListModelsView:

    def test_run_list_public_models(self):
        model = ModelFactory(privacy=Model.Privacy.PUBLIC.value)
        view = ListModelsView()
        request = get_fake_jwt_request()
        response = view.run(request, 1)
        models_response = json.loads(response.content)
        assert len(models_response['models']) == 1
        assert models_response['models'][0]['id'] == model.id
        assert models_response['models'][0]['user'] == model.user.id
        assert models_response['models'][0]['name'] == model.name
        assert models_response['models'][0]['description'] == model.description
        assert models_response['models'][0]['model_media'] == model.model_media.id
        assert models_response['models'][0]['volume'] == model.volume
        assert models_response['models'][0]['image_media'] == model.image_media.id
        assert models_response['models'][0]['privacy'] == model.privacy
        assert models_response['models'][0]['category'] == model.category

    def test_run_do_not_list_private_models(self):
        ModelFactory(privacy=Model.Privacy.PRIVATE.value)
        view = ListModelsView()
        request = get_fake_jwt_request()
        response = view.run(request, 1)
        models_response = json.loads(response.content)
        assert len(models_response['models']) == 0

    def test_run_list_models_newests_filter(self):
        model_one = ModelFactory(privacy=Model.Privacy.PUBLIC.value)
        model_two = ModelFactory(privacy=Model.Privacy.PUBLIC.value)
        view = ListModelsView()
        request = get_fake_jwt_request(get_params={'newests': ''})
        response = view.run(request, 1)
        models_response = json.loads(response.content)
        assert len(models_response['models']) == 2
        assert models_response['models'][0]['id'] == model_two.id
        assert models_response['models'][1]['id'] == model_one.id

    def test_run_list_models_most_printed_filter(self):
        model_one = ModelFactory(privacy=Model.Privacy.PUBLIC.value, printed_quantity=2)
        model_two = ModelFactory(privacy=Model.Privacy.PUBLIC.value, printed_quantity=20)
        view = ListModelsView()
        request = get_fake_jwt_request(get_params={'newests': ''})
        response = view.run(request, 1)
        models_response = json.loads(response.content)
        assert len(models_response['models']) == 2
        assert models_response['models'][0]['id'] == model_two.id
        assert models_response['models'][1]['id'] == model_one.id


@pytest.mark.django_db
class TestListModelsViewViewIntegration:

    def test_list_models(self):
        user = UserFactory()
        model_one = ModelFactory(privacy=Model.Privacy.PUBLIC.value)
        ModelFactory(privacy=Model.Privacy.PRIVATE.value)
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get('/models/', content_type='application/json', **headers)
        assert response.status_code == 200
        models_response = json.loads(response.content)
        assert len(models_response['models']) == 1
        assert models_response['models'][0]['id'] == model_one.id
        assert models_response['models'][0]['user'] == model_one.user.id
        assert models_response['models'][0]['name'] == model_one.name
        assert models_response['models'][0]['description'] == model_one.description
        assert models_response['models'][0]['model_media'] == model_one.model_media.id
        assert models_response['models'][0]['volume'] == model_one.volume
        assert models_response['models'][0]['image_media'] == model_one.image_media.id
        assert models_response['models'][0]['privacy'] == model_one.privacy
        assert models_response['models'][0]['category'] == model_one.category
