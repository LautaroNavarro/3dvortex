import pytest
import json
from django.test import Client
from model_medias.views.model_media_views.list_model_media_view import ListModelMediasView
from model_medias.tests.factories.model_media_factory import ModelMediaFactory
from helpers.testing_helpers import get_fake_jwt_request
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import ForbiddenError


@pytest.mark.django_db
class TestListModelMediasView:

    def test_validate_admin_access_success(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        view = ListModelMediasView()
        view.validate(request)

    def test_validate_admin_access_fail(self):
        user = UserFactory()
        request = get_fake_jwt_request(user=user)
        view = ListModelMediasView()
        with pytest.raises(ForbiddenError):
            view.validate(request)

    def test_run_get_model_medias(self):
        model_media = ModelMediaFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = ListModelMediasView()
        request = get_fake_jwt_request(user=user)
        response = view.run(request)
        model_media_response = json.loads(response.content)
        assert len(model_media_response['model_medias']) == 1
        assert model_media_response['model_medias'][0]['id'] == model_media.id
        assert model_media_response['model_medias'][0]['owner'] == model_media.user.email
        assert model_media_response['model_medias'][0]['url'] == model_media.url


@pytest.mark.django_db
class TestListModelMediasViewViewIntegration:

    def test_list_model_medias(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        model_media_one = ModelMediaFactory()
        model_media_two = ModelMediaFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get('/model_medias/', content_type='application/json', **headers)
        assert response.status_code == 200
        model_media_response = json.loads(response.content)
        assert len(model_media_response['model_medias']) == 2
        assert model_media_response['model_medias'][0]['id'] == model_media_one.id
        assert model_media_response['model_medias'][0]['owner'] == model_media_one.user.email
        assert model_media_response['model_medias'][0]['url'] == model_media_one.url
        assert model_media_response['model_medias'][1]['id'] == model_media_two.id
        assert model_media_response['model_medias'][1]['owner'] == model_media_two.user.email
        assert model_media_response['model_medias'][1]['url'] == model_media_two.url
