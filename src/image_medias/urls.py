from django.urls import path
from image_medias.views import ImageMediasResourceView

urlpatterns = [
    path('', ImageMediasResourceView.as_view()),
]
