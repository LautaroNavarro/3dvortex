from django.http import JsonResponse
from infra.views import BaseView
from models.models.category import Category


class ListCategoriesView(BaseView):

    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, *args, **kwargs):
        response = {
            'categories': [category.serialized for category in Category.objects.all()],
        }
        return JsonResponse(response)
