from django.views import View
from models.views.categories_view.create import CreateCategoryView


class CategoriesView(View):

    def post(self, request):
        view = CreateCategoryView()
        return view(request)
