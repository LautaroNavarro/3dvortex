import mock
import pytest
import json
from django.test import Client
from model_medias.views.model_media_views.get_model_media_by_id_view import GetModelMediaByIdView
from helpers.testing_helpers import get_fake_jwt_request
from model_medias.tests.factories.model_media_factory import ModelMediaFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from infra.request.errors import NotFoundError


@pytest.mark.django_db
class TestGetModelMediaByIdView:

    def test_validate_existing_model_media(self):
        model_media = ModelMediaFactory()
        view = GetModelMediaByIdView()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        view.validate(request, model_media_id=model_media.id)

    def test_validate_no_existing_model_media(self):
        view = GetModelMediaByIdView()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        with pytest.raises(NotFoundError):
            view.validate(request, model_media_id=-1)

    @mock.patch(
        'model_medias.views.model_media_views.get_model_media_by_id_view.validate_user_has_model_media_permission'
    )
    def test_validate_permissions_checked(self, validate_user_has_model_media_permission_mock):
        model_media = ModelMediaFactory()
        view = GetModelMediaByIdView()
        user = UserFactory()
        request = get_fake_jwt_request(user=user)
        view.validate(request, model_media_id=model_media.id)
        validate_user_has_model_media_permission_mock.assert_called_once_with(
            model_media.id,
            user.get_payload_from_jwt(user.jwt),
        )

    def test_run_get_model_media(self):
        model_media = ModelMediaFactory()
        view = GetModelMediaByIdView()
        request = get_fake_jwt_request()
        response = view.run(request, model_media_id=model_media.id)
        model_media_response = json.loads(response.content)
        assert model_media_response['id'] == model_media.id
        assert model_media_response['owner'] == model_media.user.email
        assert model_media_response['url'] == model_media.url


@pytest.mark.django_db
class TestGetModelMediaByIdViewIntegration:

    def test_get_model_media_by_id(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        model_media = ModelMediaFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/model_medias/{}'.format(model_media.id),
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        model_media_response = json.loads(response.content)
        assert model_media_response['id'] == model_media.id
        assert model_media_response['owner'] == model_media.user.email
        assert model_media_response['url'] == model_media.url
