from django.http import JsonResponse
from infra.request.errors import NotFoundError
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_jwt
from image_medias.helpers import validate_user_has_image_media_permission


class GetImageMediaByIdView(BaseView):

    @require_jwt
    def validate(self, request, image_media_id, *args, **kwargs):
        if not ImageMedia.objects.filter(id=image_media_id).exists():
            raise NotFoundError('The provided image media id does not exists')
        validate_user_has_image_media_permission(image_media_id, self.user_payload)

    def run(self, request, image_media_id, *args, **kwargs):
        return JsonResponse(ImageMedia.objects.get(id=image_media_id).serialized)
