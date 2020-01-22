import json
from django.http import JsonResponse
from infra.request.errors import (
    BadRequestError,
    ForbiddenError,
)
from infra.views import BaseView
from models.models.category import Category
from models.models.model import Model
from model_medias.models.model_media import ModelMedia
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_jwt
from users.models.user import User


class CreateModelView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'user': {'type': 'integer'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'model_media': {'type': 'integer'},
            'image_media': {'type': 'integer'},
            'privacy': {'type': 'integer'},
            'category': {'type': 'integer'},
        },
        'required': ['user', 'name', 'model_media', 'privacy', 'image_media'],
        'additionalProperties': False,
    }

    required_body = True

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if not User.objects.filter(id=body.get('user')).exists():
            raise BadRequestError('The provided user does not exist.')
        if self.user_payload['id'] != body['user'] and self.user_payload['access_level'] < User.Type.ADMIN_USER_TYPE:
            raise ForbiddenError('You can\'t create a model for this user')
        if not ModelMedia.objects.filter(id=body.get('model_media')).exists():
            raise BadRequestError('A model media with the provided model_media id does not exist.')
        if not ImageMedia.objects.filter(id=body.get('image_media')).exists():
            raise BadRequestError('A model media with the provided image_media id does not exist.')
        if not Model.Privacy.privacy_id_is_valid(body.get('privacy')):
            raise BadRequestError('The provided privacy is not valid.')
        if body.get('category') and not Category.objects.filter(id=body.get('category')).exists():
            raise BadRequestError('A category with the provided category id does not exist.')

    def run(self, request, *args, **kwargs):
        # Calculate volume
        # Create Model and assign passed parameters along with calculated volume
        body = json.loads(request.body)
        model = Model(
            user_id=body['user'],
            name=body['name'],
            description=body.get('description'),
            model_media_id=body['model_media'],
            image_media_id=body['image_media'],
            privacy=body['privacy'],
            category_id=body.get('category'),
        )
        model.volume = model.get_volume()
        dimensions = model.get_dimensions_in_mm()
        model.max_x = dimensions['x']
        model.max_y = dimensions['y']
        model.max_z = dimensions['z']
        model.save()
        return JsonResponse(model.serialized)
