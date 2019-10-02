from io import BytesIO
from django.http import JsonResponse

from infra.request.errors import BadRequestError
from infra.views import BaseView
from model_medias.models.model_media import ModelMedia
from helpers.view_helpers import require_jwt


class CreateCategoryView(BaseView):

    @require_jwt
    def validate(self, request):
        if not request.content_type == 'application/octet-stream':
            raise BadRequestError('Content type must be octet-stream.')

    def run(self, request):
        data = BytesIO(request.body)
        model_media = ModelMedia.objects.create(user_id=self.user_payload['id'])
        model_media.upload_model(data)
        return JsonResponse(model_media.serialized)
