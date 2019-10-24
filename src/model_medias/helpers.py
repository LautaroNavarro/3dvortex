from model_medias.models.model_media import ModelMedia
from infra.request.errors import ForbiddenError
from users.models.user import User


def validate_user_has_model_media_permission(image_media_id, user):
    if not user['access_level'] >= User.Type.ADMIN_USER_TYPE:
        if not ModelMedia.objects.filter(id=image_media_id, user=user['id']):
            raise ForbiddenError
