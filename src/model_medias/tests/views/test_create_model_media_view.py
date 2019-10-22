import mock
import pytest
from django.test import Client
from model_medias.views.model_media_views.create import CreateModelMediaView
from infra.request.errors import BadRequestError
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUploadImageMediasView:

    def test_validate_request_is_octet_stream(self):
        view = CreateModelMediaView()
        request = get_fake_jwt_request(content_type='application/json')
        with pytest.raises(BadRequestError):
            assert view.validate(request)

    def test_validate_request_valid_request(self):
        view = CreateModelMediaView()
        request = get_fake_jwt_request(content_type='application/octet-stream')
        request.body = {'some': 1}
        view.validate(request)

    @mock.patch('model_medias.views.model_media_views.create.ModelMedia')
    def test_run(self, model_media_model_mock):
        user = UserFactory()
        model_media_model_mock.objects.create.return_value.serialized = user.serialized
        view = CreateModelMediaView()
        data = bytes(
            "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV"
            "\xca\x00\x00\x00\x03PLTE\xffM\x00\\58\x7f\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|"
            "\xa8\x00\x00\x00\x00IEND\xaeB`\x82",
            encoding='utf8'
        )
        request = get_fake_jwt_request(user=user, content_type='application/octet-stream', body=data)
        view.user_payload = user.serialized
        view.run(request)
        model_media_model_mock.objects.create.assert_called_once_with(user_id=user.id)

        upload_model_arg_b = model_media_model_mock.objects.create.return_value.upload_model.call_args[0][0].getvalue()
        assert model_media_model_mock.objects.create.return_value.upload_model.called is True
        assert upload_model_arg_b == data


@pytest.mark.django_db
class TestUploadImageMediasViewIntegration():

    @mock.patch('model_medias.views.model_media_views.create.ModelMedia.upload_model')
    def test_upload_image(self, upload_model_mock):
        user = UserFactory()
        data = bytes(
            "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV"
            "\xca\x00\x00\x00\x03PLTE\xffM\x00\\58\x7f\x00\x00\x00\nIDATx\x9ccb\x00\x00\x00\x06\x00\x0367|"
            "\xa8\x00\x00\x00\x00IEND\xaeB`\x82",
            encoding='utf8'
        )
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        response = Client().post('/model_medias/', data, content_type='application/octet-stream', **headers)
        assert response.status_code == 200
        assert response.json()['owner'] == user.email
        # This is empty because we are mocking the method upload_image
        assert response.json()['url'] == ''
        assert upload_model_mock.called is True
        assert upload_model_mock.call_args[0][0].getvalue() == data
