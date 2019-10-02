from django.urls import path
from image_medias.views.image_media_view import ImageMediasView

urlpatterns = [
    path('', ImageMediasView.as_view()),
]
