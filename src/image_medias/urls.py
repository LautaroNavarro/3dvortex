from django.urls import path
from image_medias.views.image_media_view import (
    ImageMediasView,
    ImageMediaByIdView,
)

urlpatterns = [
    path('<int:image_media_id>', ImageMediaByIdView.as_view()),
    path('', ImageMediasView.as_view()),
]
