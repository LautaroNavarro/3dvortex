import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from models.models.category import Category
from helpers.view_helpers import require_admin


class CreateMaterialView(BaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        if not request.content_type == 'application/json':
            raise BadRequestError('Content type must be application/json.')
        if not request.body:
            raise BadRequestError('You must pass a body on the request')
        body = json.loads(request.body)
        # name validation
        if not body.get('name'):
            raise BadRequestError('You must provide a name.')
        if not (type(body.get('name')) == str):
            raise BadRequestError('Name should be a string.')
        # description validation
        if not body.get('description'):
            raise BadRequestError('You must provide a description.')
        if not (type(body.get('description')) == str):
            raise BadRequestError('Description should be a string.')
        if len(body.get('description')) > 2048:
            raise BadRequestError('Description should be smaller than 2048.')
        # price_per_kilogram validation
        if not body.get('price_per_kilogram'):
            raise BadRequestError('You must provide a price_per_kilogram.')
        if not (type(body.get('price_per_kilogram')) == str):
            raise BadRequestError('price_per_kilogram should be a string.')
        if len(body.get('price_per_kilogram')) > 2048:
            raise BadRequestError('Name should be smaller than 2048.')

        if body.get('father_category_id'):
            if not (type(body.get('father_category_id')) == int):
                raise BadRequestError('father_category_id must be an integer.')
            if not Category.objects.filter(id=body.get('father_category_id')).exists():
                raise BadRequestError('A category with the provided father_category_id does not exists.')
        if not (type(body.get('name')) == str):
            raise BadRequestError('Name should be a string.')
        if Category.objects.filter(name=body.get('name')).exists():
            raise BadRequestError('A category with the provided name already exists.')

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        category = Category.objects.create(name=body.get('name'), father_category_id=body.get('father_category_id'))
        return JsonResponse(category.serialized)
