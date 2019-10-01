from django.urls import path
from model_medias.views.model_medias_resource_view import ModelMediaResourceView

urlpatterns = [
    path('', ModelMediaResourceView.as_view()),
]
