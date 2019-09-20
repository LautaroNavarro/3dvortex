from django.urls import path
from image_medias.views import MediasResourceView

urlpatterns = [
    path('', MediasResourceView.as_view()),
]
