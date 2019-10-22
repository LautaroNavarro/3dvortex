from io import BytesIO
from django.http import JsonResponse
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_jwt


class CreateImageMediaView(BaseView):

    required_body = True

    content_type = 'application/octet-stream'

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

    def run(self, request, *args, **kwargs):
        data = BytesIO(request.body)
        image_media = ImageMedia.objects.create(user_id=self.user_payload['id'])
        image_media.upload_image(data)
        return JsonResponse(image_media.serialized)
