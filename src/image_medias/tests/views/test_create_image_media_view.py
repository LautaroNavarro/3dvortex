import mock
import pytest
from django.test import Client
from image_medias.views.image_media_views.create_image_media_view import CreateImageMediaView
from infra.request.errors import BadRequestError
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUploadImageMediasView:

    def test_validate_request_is_octet_stream(self):
        view = CreateImageMediaView()
        request = get_fake_jwt_request(content_type='application/json')
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_request_valid_request(self):
        view = CreateImageMediaView()
        request = get_fake_jwt_request(content_type='application/octet-stream')
        request.body = True
        view.validate(request)

    @mock.patch('image_medias.views.image_media_views.create_image_media_view.ImageMedia')
    def test_run(self, image_media_model_mock):
        user = UserFactory()
        image_media_model_mock.objects.create.return_value.serialized = user.serialized
        view = CreateImageMediaView()
        data = bytes(
            "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV"
            "\xca\x00\x00\x00\x03PLTE\xffM\x00\\58\x7f\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|"
            "\xa8\x00\x00\x00\x00IEND\xaeB`\x82",
            encoding='utf8'
        )
        request = get_fake_jwt_request(user=user, content_type='application/octet-stream', body=data)
        view.user_payload = user.serialized
        view.run(request)
        image_media_model_mock.objects.create.assert_called_once_with(user_id=user.id)

        upload_image_arg_b = image_media_model_mock.objects.create.return_value.upload_image.call_args[0][0].getvalue()
        assert image_media_model_mock.objects.create.return_value.upload_image.called is True
        assert upload_image_arg_b == data


@pytest.mark.django_db
class TestUploadImageMediasViewIntegration():

    @mock.patch('image_medias.views.image_media_views.create_image_media_view.ImageMedia.upload_image')
    def test_upload_image(self, upload_image_mock):
        user = UserFactory()
        data = bytes(
            "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV"
            "\xca\x00\x00\x00\x03PLTE\xffM\x00\\58\x7f\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|"
            "\xa8\x00\x00\x00\x00IEND\xaeB`\x82",
            encoding='utf8'
        )
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().post('/image_medias/', data, content_type='application/octet-stream', **headers)
        assert response.status_code == 200
        assert response.json()['owner'] == user.email
        # This is empty because we are mocking the method upload_image
        assert response.json()['url'] == ''
        assert upload_image_mock.called is True
        assert upload_image_mock.call_args[0][0].getvalue() == data
