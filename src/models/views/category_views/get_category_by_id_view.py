from django.http import JsonResponse
from infra.request.errors import NotFoundError
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_jwt


class GetCategoryByIdView(BaseView):

    @require_jwt
    def validate(self, request, category_id, *args, **kwargs):
        if not Category.objects.filter(id=category_id).exists():
            raise NotFoundError('The provided category id does not exists')

    def run(self, request, category_id, *args, **kwargs):
        return JsonResponse(Category.objects.get(id=category_id).serialized)
