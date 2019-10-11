from django.views import View
from models.views.category_views.create_category_view import CreateCategoryView
from models.views.category_views.get_category_by_id_view import GetCategoryByIdView


class CategoriesView(View):

    def post(self, request, *args, **kwargs):
        view = CreateCategoryView()
        return view(request, *args, **kwargs)


class CategoriesByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetCategoryByIdView()
        return view(request, *args, **kwargs)
