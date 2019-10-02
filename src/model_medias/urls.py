from django.urls import path
from model_medias.views.model_media_view import ModelMediaView

urlpatterns = [
    path('', ModelMediaView.as_view()),
]
