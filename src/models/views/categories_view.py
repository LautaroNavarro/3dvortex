from django.views import View
from models.views.category_views.create_category_view import CreateCategoryView


class CategoriesView(View):

    def post(self, request):
        view = CreateCategoryView()
        return view(request)
