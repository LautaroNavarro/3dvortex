from django.urls import path
from prints.views.materials_view import (
    MaterialsView,
    MaterialsByIdView
)


BASE_MATERIAL_URL = 'materials/{}'
BASE_PRINTS_URL = 'prints/{}'

urlpatterns = [
    path(BASE_MATERIAL_URL.format(''), MaterialsView.as_view()),
    path(BASE_MATERIAL_URL.format('<int:material_id>'), MaterialsByIdView.as_view()),
]
