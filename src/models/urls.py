from django.urls import path
from image_medias.views.image_media_view import ImageMediasView

BASE_MODEL_URL = 'models/{}'
BASE_CATEGORY_URL = 'categories/{}'

urlpatterns = [
    path(BASE_CATEGORY_URL, ImageMediasView.as_view()),
]
