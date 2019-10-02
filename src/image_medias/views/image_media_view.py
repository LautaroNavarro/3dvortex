from django.views import View
from image_medias.views.image_media_views.create import CreateImageMediaView


class ImageMediasView(View):

    def post(self, request):
        view = CreateImageMediaView()
        return view(request)
