from django.urls import path
from model_medias.views.model_media_view import (
    ModelMediaView,
    ModelMediaByIdView,
)

urlpatterns = [
    path('', ModelMediaView.as_view()),
    path('<int:model_media_id>', ModelMediaByIdView.as_view()),
]
