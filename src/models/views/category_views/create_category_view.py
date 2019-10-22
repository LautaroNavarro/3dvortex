import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_admin


class CreateCategoryView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'father_category_id': {'type': 'integer'},
        },
        'required': ['name'],
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if body.get('father_category_id'):
            if not Category.objects.filter(id=body.get('father_category_id')).exists():
                raise BadRequestError('A category with the provided father_category_id does not exists.')
        if Category.objects.filter(name=body.get('name')).exists():
            raise BadRequestError('A category with the provided name already exists.')

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        category = Category.objects.create(name=body.get('name'), father_category_id=body.get('father_category_id'))
        return JsonResponse(category.serialized)
