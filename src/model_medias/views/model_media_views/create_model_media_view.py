from io import BytesIO
from django.http import JsonResponse

from infra.views import BaseView
from model_medias.models.model_media import ModelMedia
from helpers.view_helpers import require_jwt


class CreateModelMediaView(BaseView):

    content_type = 'application/octet-stream'

    required_body = True

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

    def run(self, request, *args, **kwargs):
        data = BytesIO(request.body)
        model_media = ModelMedia.objects.create(user_id=self.user_payload['id'])
        model_media.upload_model(data)
        return JsonResponse(model_media.serialized)
