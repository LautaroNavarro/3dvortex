from django.views import View
from model_medias.views.model_media_views.create import CreateModelMediaView


class ModelMediaView(View):

    def post(self, request):
        view = CreateModelMediaView()
        return view(request)
