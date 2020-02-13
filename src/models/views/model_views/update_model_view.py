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


class UpdateModelView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'model_media': {'type': 'integer'},
            'image_media': {'type': 'integer'},
            'privacy': {'type': 'integer'},
            'category': {'type': 'integer'},
        },
        'additionalProperties': False,
    }

    required_body = True

    @require_jwt
    def validate(self, request, model_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        model = Model.objects.filter(id=model_id)
        if len(model) == 0:
            raise BadRequestError('The provided model does not exist.')
        if (
            self.user_payload['id'] != model[0].user_id and
            self.user_payload['access_level'] < User.Type.ADMIN_USER_TYPE
        ):
            raise ForbiddenError('You can\'t update this model.')
        if body.get('model_media') and not ModelMedia.objects.filter(id=body.get('model_media')).exists():
            raise BadRequestError('A model media with the provided model_media id does not exist.')
        if body.get('image_media') and not ImageMedia.objects.filter(id=body.get('image_media')).exists():
            raise BadRequestError('A model media with the provided image_media id does not exist.')
        if body.get('privacy') and not Model.Privacy.privacy_id_is_valid(body.get('privacy')):
            raise BadRequestError('The provided privacy is not valid.')
        if (
            body.get('category') and
            body.get('category') and
            not Category.objects.filter(id=body.get('category')).exists()
        ):
            raise BadRequestError('A category with the provided category id does not exist.')

    def run(self, request, model_id, *args, **kwargs):
        parameters = json.loads(request.body)
        model = Model.objects.filter(id=model_id)
        model.update(**parameters)
        return JsonResponse(model[0].serialized)
