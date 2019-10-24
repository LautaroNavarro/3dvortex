from image_medias.models.image_media import ImageMedia
from infra.request.errors import ForbiddenError
from users.models.user import User


def validate_user_has_image_media_permission(image_media_id, user):
    if not user['access_level'] >= User.Type.ADMIN_USER_TYPE:
        if not ImageMedia.objects.filter(id=image_media_id, user=user['id']):
            raise ForbiddenError
