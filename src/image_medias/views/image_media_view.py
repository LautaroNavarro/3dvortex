from django.views import View
from image_medias.views.image_media_views.create_image_media_view import CreateImageMediaView
from image_medias.views.image_media_views.list_image_medias_view import ListImageMediasView
from image_medias.views.image_media_views.get_image_media_by_id_view import GetImageMediaByIdView
from image_medias.views.image_media_views.create_image_media_from_url import CreateImageMediaFromUrlView


class ImageMediasView(View):

    def post(self, request, *args, **kwargs):
        view = CreateImageMediaView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListImageMediasView()
        return view(request, *args, **kwargs)


class ImageMediaByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetImageMediaByIdView()
        return view(request, *args, **kwargs)


class ImageMediaFromUrl(View):

    def post(self, request, *args, **kwargs):
        view = CreateImageMediaFromUrlView()
        return view(request, *args, **kwargs)
