from django.views import View
from models.views.category_views.create_category_view import CreateCategoryView
from models.views.category_views.get_category_by_id_view import GetCategoryByIdView
from models.views.category_views.list_categories_view import ListCategoriesView
from models.views.category_views.update_category_view import UpdateCategoryView


class CategoriesView(View):

    def post(self, request, *args, **kwargs):
        view = CreateCategoryView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListCategoriesView()
        return view(request, *args, **kwargs)


class CategoriesByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetCategoryByIdView()
        return view(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        view = UpdateCategoryView()
        return view(request, *args, **kwargs)
