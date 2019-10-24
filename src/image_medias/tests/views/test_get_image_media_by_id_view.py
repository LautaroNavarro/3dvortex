import mock
import pytest
import json
from django.test import Client
from image_medias.views.image_media_views.get_image_media_by_id_view import GetImageMediaByIdView
from helpers.testing_helpers import get_fake_jwt_request
from image_medias.tests.factories.image_media_factory import ImageMediaFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from infra.request.errors import NotFoundError


@pytest.mark.django_db
class TestGetImageMediaByIdView:

    def test_validate_existing_image_media(self):
        image_media = ImageMediaFactory()
        view = GetImageMediaByIdView()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        view.validate(request, image_media_id=image_media.id)

    def test_validate_no_existing_image_media(self):
        view = GetImageMediaByIdView()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        with pytest.raises(NotFoundError):
            view.validate(request, image_media_id=-1)

    @mock.patch(
        'image_medias.views.image_media_views.get_image_media_by_id_view.validate_user_has_image_media_permission'
    )
    def test_validate_permissions_checked(self, validate_user_has_image_media_permission_mock):
        image_media = ImageMediaFactory()
        view = GetImageMediaByIdView()
        user = UserFactory()
        request = get_fake_jwt_request(user=user)
        view.validate(request, image_media_id=image_media.id)
        validate_user_has_image_media_permission_mock.assert_called_once_with(
            image_media.id,
            user.get_payload_from_jwt(user.jwt),
        )

    def test_run_get_image_media(self):
        image_media = ImageMediaFactory()
        view = GetImageMediaByIdView()
        request = get_fake_jwt_request()
        response = view.run(request, image_media_id=image_media.id)
        image_media_response = json.loads(response.content)
        assert image_media_response['id'] == image_media.id
        assert image_media_response['owner'] == image_media.user.email
        assert image_media_response['url'] == image_media.url


@pytest.mark.django_db
class TestGetImageMediaByIdViewIntegration:

    def test_get_image_media_by_id(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        image_media = ImageMediaFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get(
            '/image_medias/{}'.format(image_media.id),
            content_type='application/json',
            **headers
        )
        assert response.status_code == 200
        image_media_response = json.loads(response.content)
        assert image_media_response['id'] == image_media.id
        assert image_media_response['owner'] == image_media.user.email
        assert image_media_response['url'] == image_media.url
