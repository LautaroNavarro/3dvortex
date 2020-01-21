from django.http import JsonResponse
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_jwt
from infra.request.errors import BadRequestError


class CreateImageMediaView(BaseView):

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not request.FILES.get('content'):
            raise BadRequestError('You must provide a image file')

    def run(self, request, *args, **kwargs):
        data = request.FILES['content']
        image_media = ImageMedia.objects.create(user_id=self.user_payload['id'])
        image_media.upload_image(data)
        return JsonResponse(image_media.serialized)
