from django.http import JsonResponse
from infra.views import BaseView
from model_medias.models.model_media import ModelMedia
from helpers.view_helpers import require_admin


class ListModelMediasView(BaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, *args, **kwargs):
        return JsonResponse({
            'model_medias': [image_media.serialized for image_media in ModelMedia.objects.all()]
        })
