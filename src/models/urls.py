from django.urls import path
from models.views.categories_view import CategoriesView

BASE_MODEL_URL = 'models/{}'
BASE_CATEGORY_URL = 'categories/{}'

urlpatterns = [
    path(BASE_CATEGORY_URL.format(''), CategoriesView.as_view()),
]
