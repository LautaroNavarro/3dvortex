from django.http import JsonResponse
from infra.request.errors import NotFoundError
from infra.views import BaseView
from model_medias.models.model_media import ModelMedia
from helpers.view_helpers import require_jwt
from model_medias.helpers import validate_user_has_model_media_permission


class GetModelMediaByIdView(BaseView):

    @require_jwt
    def validate(self, request, model_media_id, *args, **kwargs):
        if not ModelMedia.objects.filter(id=model_media_id).exists():
            raise NotFoundError('The provided image media id does not exists')
        validate_user_has_model_media_permission(model_media_id, self.user_payload)

    def run(self, request, model_media_id, *args, **kwargs):
        return JsonResponse(ModelMedia.objects.get(id=model_media_id).serialized)
