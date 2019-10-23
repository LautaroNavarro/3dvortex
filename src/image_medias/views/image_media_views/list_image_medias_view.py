from django.http import JsonResponse
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_admin


class ListImageMediasView(BaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, *args, **kwargs):
        return JsonResponse({
            'image_medias': [image_media.serialized for image_media in ImageMedia.objects.all()]
        })
