from django.http import JsonResponse

import json
from infra.views import BaseView
from image_medias.models.image_media import ImageMedia
from helpers.view_helpers import require_admin
from infra.request.errors import BadRequestError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CreateImageMediaFromUrlView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'url': {'type': 'string'},
        },
        'required': ['url'],
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        val = URLValidator()
        try:
            val(body['url'])
        except ValidationError:
            raise BadRequestError('Not valid URL.')

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        image_media = ImageMedia.objects.create(
            user_id=self.user_payload['id'],
            url=body['url']
        )
        return JsonResponse(image_media.serialized)
