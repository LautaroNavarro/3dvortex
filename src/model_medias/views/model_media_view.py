from django.views import View
from model_medias.views.model_media_views.create_model_media_view import CreateModelMediaView
from model_medias.views.model_media_views.list_model_media_view import ListModelMediasView
from model_medias.views.model_media_views.get_model_media_by_id_view import GetModelMediaByIdView
from model_medias.views.model_media_views.create_model_media_from_url import CreateModelMediaFromUrlView


class ModelMediaView(View):

    def post(self, request, *args, **kwargs):
        view = CreateModelMediaView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListModelMediasView()
        return view(request, *args, **kwargs)


class ModelMediaByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetModelMediaByIdView()
        return view(request, *args, **kwargs)


class ModelMediaFromUrl(View):

    def post(self, request, *args, **kwargs):
        view = CreateModelMediaFromUrlView()
        return view(request, *args, **kwargs)
