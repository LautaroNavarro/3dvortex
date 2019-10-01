from django.views import View
from model_medias.views.upload_model_media_view import UploadModelMediaView


class ModelMediaResourceView(View):

    def post(self, request):
        view = UploadModelMediaView()
        return view(request)
