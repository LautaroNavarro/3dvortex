import pytest
from infra.request.errors import ForbiddenError
from model_medias.tests.factories.model_media_factory import ModelMediaFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from model_medias.helpers import validate_user_has_model_media_permission


@pytest.mark.django_db
class TestValidateUserHasModelMediaPermissions:

    def test_raise_error_if_not_admin_user_and_not_owner(self):
        model_media = ModelMediaFactory()
        not_admin_user = UserFactory()
        with pytest.raises(ForbiddenError):
            validate_user_has_model_media_permission(
                model_media.id,
                not_admin_user.get_payload_from_jwt(not_admin_user.jwt),
            )

    def test_not_raise_error_if_not_admin_user_and_owner(self):
        not_admin_user = UserFactory()
        model_media = ModelMediaFactory(user=not_admin_user)
        validate_user_has_model_media_permission(
            model_media.id,
            not_admin_user.get_payload_from_jwt(not_admin_user.jwt),
        )

    def test_not_raise_error_if_admin_user_and_not_owner(self):
        admin_user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        model_media = ModelMediaFactory()
        validate_user_has_model_media_permission(
            model_media.id,
            admin_user.get_payload_from_jwt(admin_user.jwt),
        )

    def test_not_raise_error_if_admin_user_and_owner(self):
        admin_user = UserFactory()
        model_media = ModelMediaFactory(user=admin_user)
        validate_user_has_model_media_permission(
            model_media.id,
            admin_user.get_payload_from_jwt(admin_user.jwt),
        )
