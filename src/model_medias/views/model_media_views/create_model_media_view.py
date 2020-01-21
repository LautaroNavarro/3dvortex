from django.http import JsonResponse

from infra.views import BaseView
from model_medias.models.model_media import ModelMedia
from helpers.view_helpers import require_jwt
from infra.request.errors import BadRequestError


class CreateModelMediaView(BaseView):

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not request.FILES.get('content'):
            raise BadRequestError('You must provide a model file')

    def run(self, request, *args, **kwargs):
        data = request.FILES['content']
        model_media = ModelMedia.objects.create(user_id=self.user_payload['id'])
        model_media.upload_model(data)
        return JsonResponse(model_media.serialized)
