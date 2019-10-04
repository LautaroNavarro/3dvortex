import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_admin


class CreateCategoryView(BaseView):

    @require_admin
    def validate(self, request):
        if not request.content_type == 'application/json':
            raise BadRequestError('Content type must be application/json.')
        if not request.body:
            raise BadRequestError('You must pass a body on the request')
        body = json.loads(request.body)
        if not body.get('name'):
            raise BadRequestError('You must provide a name.')
        if not (type(body.get('name')) == str):
            raise BadRequestError('Name should be a string.')
        if body.get('father_category'):
            if not (type(body.get('father_category')) == int):
                raise BadRequestError('father_category must be an integer.')
            if not Category.objects.filter(id=body.get('father_category')).exists():
                raise BadRequestError('A category with the provided father_category does not exists.')
        if not (type(body.get('name')) == str):
            raise BadRequestError('Name should be a string.')
        if Category.objects.filter(name=body.get('name')).exists():
            raise BadRequestError('A category with the provided name already exists.')

    def run(self, request):
        body = json.loads(request.body)
        category = Category.objects.create(name=body.get('name'), father_category_id=body.get('father_category'))
        return JsonResponse(category.serialized)
