import pytest
import json
from django.test import Client
from image_medias.views.image_media_views.list_image_medias_view import ListImageMediasView
from image_medias.tests.factories.image_media_factory import ImageMediaFactory
from helpers.testing_helpers import get_fake_jwt_request
from users.models.user import User
from users.tests.factories.user_factory import UserFactory
from infra.request.errors import ForbiddenError


@pytest.mark.django_db
class TestListImageMediasView:

    def test_validate_admin_access_success(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        request = get_fake_jwt_request(user=user)
        view = ListImageMediasView()
        view.validate(request)

    def test_validate_admin_access_fail(self):
        user = UserFactory()
        request = get_fake_jwt_request(user=user)
        view = ListImageMediasView()
        with pytest.raises(ForbiddenError):
            view.validate(request)

    def test_run_get_image_medias(self):
        image_media = ImageMediaFactory()
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = ListImageMediasView()
        request = get_fake_jwt_request(user=user)
        response = view.run(request)
        image_media_response = json.loads(response.content)
        assert len(image_media_response['image_medias']) == 1
        assert image_media_response['image_medias'][0]['id'] == image_media.id
        assert image_media_response['image_medias'][0]['owner'] == image_media.user.email
        assert image_media_response['image_medias'][0]['url'] == image_media.url


@pytest.mark.django_db
class TestListImageMediasViewViewIntegration:

    def test_list_image_medias(self):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        image_media_one = ImageMediaFactory()
        image_media_two = ImageMediaFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().get('/image_medias/', content_type='application/json', **headers)
        assert response.status_code == 200
        image_media_response = json.loads(response.content)
        assert len(image_media_response['image_medias']) == 2
        assert image_media_response['image_medias'][0]['id'] == image_media_one.id
        assert image_media_response['image_medias'][0]['owner'] == image_media_one.user.email
        assert image_media_response['image_medias'][0]['url'] == image_media_one.url
        assert image_media_response['image_medias'][1]['id'] == image_media_two.id
        assert image_media_response['image_medias'][1]['owner'] == image_media_two.user.email
        assert image_media_response['image_medias'][1]['url'] == image_media_two.url
