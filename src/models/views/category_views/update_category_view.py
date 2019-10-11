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

    @require_admin
    def validate(self, request, category_id, *args, **kwargs):
        if not request.content_type == 'application/json':
            raise BadRequestError('Content type must be application/json.')
        if not request.body:
            raise BadRequestError('You must pass a body on the request')
        if not Category.objects.filter(id=category_id).exists():
            raise NotFoundError('The provided category id does not exists')
        body = json.loads(request.body)
        if body.get('name'):
            if not (type(body.get('name')) == str):
                raise BadRequestError('Name should be a string.')
        if body.get('father_category_id'):
            if not (type(body.get('father_category_id')) == int):
                raise BadRequestError('father_category_id must be an integer.')
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
