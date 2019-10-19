from django.http import JsonResponse
from infra.request.errors import (
    BadRequestError,
    NotFoundError,
)
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_admin


class DeleteCategoryView(BaseView):

    @require_admin
    def validate(self, request, category_id, *args, **kwargs):
        if not request.content_type == 'application/json':
            raise BadRequestError('Content type must be application/json.')
        if not Category.objects.filter(id=category_id).exists():
            raise NotFoundError('The provided category id does not exists')

    def run(self, request, category_id, *args, **kwargs):
        Category.objects.filter(id=category_id).delete()
        return JsonResponse({'deleted': True})
