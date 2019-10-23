from django.views import View
from image_medias.views.image_media_views.create_image_media_view import CreateImageMediaView
from image_medias.views.image_media_views.list_image_medias_view import ListImageMediasView


class ImageMediasView(View):

    def post(self, request, *args, **kwargs):
        view = CreateImageMediaView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListImageMediasView()
        return view(request, *args, **kwargs)
