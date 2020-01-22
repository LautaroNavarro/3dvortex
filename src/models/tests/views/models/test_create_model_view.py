import mock
import json
import pytest
from django.test import Client
from helpers.testing_helpers import get_fake_jwt_request
from models.views.model_views.create_model_view import CreateModelView
from models.tests.factories.category_factory import CategoryFactory
from models.models.model import Model
from infra.request.errors import (
    ForbiddenError,
    BadRequestError,
)
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from model_medias.tests.factories.model_media_factory import ModelMediaFactory
from image_medias.tests.factories.image_media_factory import ImageMediaFactory


@mock.patch('models.models.model.Model.get_dimensions_in_mm')
@mock.patch('models.models.model.Model.get_volume')
@pytest.mark.django_db
class TestCreateModelView:

    def test_validate_not_valid_content_type(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        request = get_fake_jwt_request(user=user, content_type='not valid ct')
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_body_is_provided_on_request(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        request = get_fake_jwt_request(user)
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_privacy_is_not_provided(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy', 'image_media']
        request = get_fake_jwt_request(user, body=json.dumps({'user': user.id, 'name': 'Model name', 'model_media': 1}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_user_is_not_provided(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy', 'image_media']
        request = get_fake_jwt_request(user, body=json.dumps(
            {'privacy': user.id, 'name': 'Model name', 'model_media': 1}
        ))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_name_is_not_provided(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy', 'image_media']
        request = get_fake_jwt_request(user, body=json.dumps({'user': user.id, 'privacy': 1, 'model_media': 1}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_model_media_is_not_provided(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy', 'image_media']
        request = get_fake_jwt_request(user, body=json.dumps({'user': user.id, 'privacy': 1, 'name': 'model name'}))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_image_media_is_not_provided(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        # Required fields = ['user', 'name', 'model_media', 'privacy', 'image_media']
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': 1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_user_id(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        image_media = ImageMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': -1,
            'privacy': 1,
            'name': 'model name',
            'model_media': 1,
            'image_media': image_media.id,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_model_media(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        image_media = ImageMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': -1,
            'image_media': image_media.id,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_image_media(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'image_media': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_privacy(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        image_media = ImageMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': -1,
            'name': 'model name',
            'image_media': image_media.id,
            'model_media': model_media.id,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_invalid_category(self, mock_get_volume, mock_get_dimensions):
        user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        view = CreateModelView()
        model_media = ModelMediaFactory()
        image_media = ImageMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'image_media': image_media.id,
            'category': -1,
        }))
        with pytest.raises(BadRequestError):
            view.validate(request)

    def test_validate_raise_error_when_user_try_to_create_model_for_other_user_and_no_permissions(
        self,
        mock_get_volume,
        mock_get_dimensions,
    ):
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        user_two = UserFactory()
        view = CreateModelView()
        model_media = ModelMediaFactory()
        image_media = ImageMediaFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user_two.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'image_media': image_media.id,
        }))
        with pytest.raises(ForbiddenError):
            view.validate(request)

    def test_run_create_and_return_object(self, mock_get_volume, mock_get_dimensions):
        mock_get_volume.return_value = 123
        mock_get_dimensions.return_value = {
            'x': 1,
            'y': 2,
            'z': 3,
        }
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        view = CreateModelView()
        image_media = ImageMediaFactory()
        model_media = ModelMediaFactory()
        category = CategoryFactory()
        request = get_fake_jwt_request(user, body=json.dumps({
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'image_media': image_media.id,
            'description': 'So good description',
            'category': category.id,
        }))
        response = view.run(request)
        assert response.status_code == 200
        response_body = json.loads(response.content)
        assert response_body['user'] == user.id
        assert response_body['privacy'] == 1
        assert response_body['name'] == 'model name'
        assert response_body['model_media']['id'] == model_media.id
        assert response_body['model_media']['url'] == model_media.url
        assert response_body['image_media']['id'] == image_media.id
        assert response_body['image_media']['url'] == image_media.url
        assert response_body['description'] == 'So good description'
        assert response_body['category'] == category.id
        assert response_body['max_x'] == '1'
        assert response_body['max_y'] == '2'
        assert response_body['max_z'] == '3'
        assert response_body['volume'] == '123'
        assert Model.objects.filter(id=response_body['id']).exists() is True


@mock.patch('models.models.model.Model.get_dimensions_in_mm')
@mock.patch('models.models.model.Model.get_volume')
@pytest.mark.django_db
class TestCreateModelViewIntegration():

    def test_create_model(self, mock_get_volume, mock_get_dimensions):
        mock_get_volume.return_value = 123
        mock_get_dimensions.return_value = {
            'x': 1,
            'y': 2,
            'z': 3,
        }
        user = UserFactory(access_level=User.Type.COMMON_USER_TYPE)
        model_media = ModelMediaFactory()
        image_media = ImageMediaFactory()
        category = CategoryFactory()
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(user.jwt)}
        data = {
            'user': user.id,
            'privacy': 1,
            'name': 'model name',
            'model_media': model_media.id,
            'image_media': image_media.id,
            'description': 'So good description',
            'category': category.id,
        }
        response = Client().post('/models/', data, content_type='application/json', **headers)
        assert response.status_code == 200
        assert response.json().get('user') == user.id
