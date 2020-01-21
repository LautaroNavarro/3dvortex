import mock
import pytest
from django.test import Client
from image_medias.views.image_media_views.create_image_media_view import CreateImageMediaView
from infra.request.errors import BadRequestError
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUploadImageMediasView:

    def test_validate_request_valid_request(self):
        view = CreateImageMediaView()
        FILES = {'content': 'otro manso file'}
        request = get_fake_jwt_request(files=FILES)
        request.body = True
        view.validate(request)

    @mock.patch('image_medias.views.image_media_views.create_image_media_view.ImageMedia')
    def test_run(self, image_media_model_mock):
        user = UserFactory()
        image_media_model_mock.objects.create.return_value.serialized = user.serialized
        view = CreateImageMediaView()
        FILES = {'content': 'manso file'}
        request = get_fake_jwt_request(
            user=user,
            files=FILES,
        )
        view.user_payload = user.serialized
        view.run(request)
        image_media_model_mock.objects.create.assert_called_once_with(user_id=user.id)
        uploaded_image_file = image_media_model_mock.objects.create.return_value.upload_image.call_args[0][0]
        assert image_media_model_mock.objects.create.return_value.upload_image.called is True
        assert uploaded_image_file == 'manso file'


@pytest.mark.django_db
class TestUploadImageMediasViewIntegration():

    @mock.patch('image_medias.views.image_media_views.create_image_media_view.ImageMedia.upload_image')
    def test_upload_image(self, upload_image_mock):
        user = UserFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        with open('./image_medias/tests/views/image.png') as image:
            response = Client().post(
                '/image_medias/',
                {'content': image},
                **headers
            )
        assert response.status_code == 200
        assert response.json()['owner'] == user.email
        # This is empty because we are mocking the method upload_image
        assert response.json()['url'] == ''
        assert upload_image_mock.called is True
