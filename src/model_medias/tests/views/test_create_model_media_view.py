import mock
import pytest
from django.test import Client
from model_medias.views.model_media_views.create_model_media_view import CreateModelMediaView
from infra.request.errors import BadRequestError
from helpers.testing_helpers import get_fake_jwt_request
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestUploadImageMediasView:

    def test_validate_request_valid_request(self):
        view = CreateModelMediaView()
        FILES = {'content': 'otro manso file'}
        request = get_fake_jwt_request(files=FILES)
        request.body = True
        view.validate(request)

    @mock.patch('model_medias.views.model_media_views.create_model_media_view.ModelMedia')
    def test_run(self, model_media_model_mock):
        user = UserFactory()
        model_media_model_mock.objects.create.return_value.serialized = user.serialized
        view = CreateModelMediaView()
        FILES = {'content': 'manso file'}
        request = get_fake_jwt_request(
            user=user,
            files=FILES,
        )
        view.user_payload = user.serialized
        view.run(request)
        model_media_model_mock.objects.create.assert_called_once_with(user_id=user.id)
        uploaded_image_file = model_media_model_mock.objects.create.return_value.upload_model.call_args[0][0]
        assert model_media_model_mock.objects.create.return_value.upload_model.called is True
        assert uploaded_image_file == 'manso file'


@pytest.mark.django_db
class TestUploadImageMediasViewIntegration():

    @mock.patch('model_medias.views.model_media_views.create_model_media_view.ModelMedia.upload_model')
    def test_upload_image(self, upload_model_mock):
        user = UserFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        with open('./model_medias/tests/views/model.stl') as model:
            response = Client().post(
                '/model_medias/',
                {'content': model},
                **headers
            )
        assert response.status_code == 200
        assert response.json()['owner'] == user.email
        # This is empty because we are mocking the method upload_image
        assert response.json()['url'] == ''
        assert upload_model_mock.called is True
        assert upload_model_mock.call_args[0][0].name == 'model.stl'
