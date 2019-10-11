from django.urls import path
from models.views.categories_view import CategoriesView
from models.views.categories_view import CategoriesByIdView


BASE_MODEL_URL = 'models/{}'
BASE_CATEGORY_URL = 'categories/{}'

urlpatterns = [
    path(BASE_CATEGORY_URL.format(''), CategoriesView.as_view()),
    path(BASE_CATEGORY_URL.format('<int:category_id>'), CategoriesByIdView.as_view()),
]
