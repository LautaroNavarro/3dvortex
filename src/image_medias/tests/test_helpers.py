import pytest
from infra.request.errors import ForbiddenError
from image_medias.tests.factories.image_media_factory import ImageMediaFactory
from users.tests.factories.user_factory import UserFactory
from users.models.user import User
from image_medias.helpers import validate_user_has_image_media_permission


@pytest.mark.django_db
class TestValidateUserHasImageMediaPermissions:

    def test_raise_error_if_not_admin_user_and_not_owner(self):
        image_media = ImageMediaFactory()
        not_admin_user = UserFactory()
        with pytest.raises(ForbiddenError):
            validate_user_has_image_media_permission(
                image_media.id,
                not_admin_user.get_payload_from_jwt(not_admin_user.jwt),
            )

    def test_not_raise_error_if_not_admin_user_and_owner(self):
        not_admin_user = UserFactory()
        image_media = ImageMediaFactory(user=not_admin_user)
        validate_user_has_image_media_permission(
            image_media.id,
            not_admin_user.get_payload_from_jwt(not_admin_user.jwt),
        )

    def test_not_raise_error_if_admin_user_and_not_owner(self):
        admin_user = UserFactory(access_level=User.Type.ADMIN_USER_TYPE)
        image_media = ImageMediaFactory()
        validate_user_has_image_media_permission(
            image_media.id,
            admin_user.get_payload_from_jwt(admin_user.jwt),
        )

    def test_not_raise_error_if_admin_user_and_owner(self):
        admin_user = UserFactory()
        image_media = ImageMediaFactory(user=admin_user)
        validate_user_has_image_media_permission(
            image_media.id,
            admin_user.get_payload_from_jwt(admin_user.jwt),
        )
