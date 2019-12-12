import json
from django.http import JsonResponse
from infra.request.errors import BadRequestError
from infra.views import BaseView
from models.models.category import Category
from models.models.model import Model
from helpers.view_helpers import require_jwt
from users.models.user import User


# volume
# image_media

class CreateModelView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'user': {'type': 'integer'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'model_media': {'type': 'integer'},
            'privacy': {'type': 'integer'},
            'category': {'type': 'integer'},
        },
        'required': ['user', 'name', 'model_media', 'privacy'],
        'additionalProperties': False,
    }

    required_body = True

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if not User.objects.filter(id=body.get('user')).exists():
            raise BadRequestError('The provided user does not exist.')
        if not Model.objects.filter(id=body.get('model_media')).exists():
            raise BadRequestError('A model media with the provided model_media id does not exist.')
        if body.get('category') and not Category.objects.filter(id=body.get('category')).exists():
            raise BadRequestError('A category with the provided category id does not exist.')
        if not Model.Privacy.privacy_id_is_valid(body.get('privacy')):
            raise BadRequestError('The provided privacy is not valid.')

    def run(self, request, *args, **kwargs):
        # Calculate volume
        # Render model, upload image to s3, and create ImageMedia
        # Create Model and assign passed parameters along with calculated volume and ImageMedia
        body = json.loads(request.body)
        return JsonResponse()
