import json
from django.http import JsonResponse
from infra.request.errors import (
    BadRequestError,
    NotFoundError,
)
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_admin


class UpdateCategoryView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'father_category_id': {'type': 'integer'},
        },
        'required': [],
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, category_id, *args, **kwargs):
        super().validate(request, category_id, *args, **kwargs)
        if not Category.objects.filter(id=category_id).exists():
            raise NotFoundError('The provided category id does not exists')
        body = json.loads(request.body)
        if body.get('father_category_id'):
            if not Category.objects.filter(id=body.get('father_category_id')).exists():
                raise BadRequestError('A category with the provided father_category_id does not exists.')
        if Category.objects.filter(name=body.get('name')).exists():
            raise BadRequestError('A category with the provided name already exists.')

    def run(self, request, category_id, *args, **kwargs):
        body = json.loads(request.body)
        update_args = {}
        if body.get('name'):
            update_args['name'] = body.get('name')
        if body.get('father_category_id'):
            update_args['father_category_id'] = body.get('father_category_id')
        Category.objects.filter(id=category_id).update(**update_args)
        return JsonResponse(Category.objects.get(id=category_id).serialized)
