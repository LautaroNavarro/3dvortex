from django.http import JsonResponse
from infra.request.errors import (
    NotFoundError,
    ForbiddenError,
    BadRequestError,
)
from users.models.user import User
from infra.views import BaseView
from models.models.model import Model
from helpers.view_helpers import require_jwt
from prints.models.material import Material


class GetModelPrice(BaseView):

    @require_jwt
    def validate(self, request, model_id, *args, **kwargs):
        super().validate(request, model_id, *args, **kwargs)
        model = Model.objects.filter(id=model_id)
        if not model:
            raise NotFoundError('The provided model id does not exists')
        if (
            model[0].user.id != self.user_payload['id'] and
            self.user_payload['access_level'] < User.Type.ADMIN_USER_TYPE.value
        ):
            raise ForbiddenError('You are not allowed to calculated price for the request model')

        if not request.GET.get('material_id') or not request.GET.get('scale'):
            raise BadRequestError('New query params: material_id, scale')
        if not Material.objects.filter(id=request.GET['material_id']).exists():
            raise BadRequestError('Invalid material id.')

    def run(self, request, model_id, *args, **kwargs):
        material = Material.objects.get(id=request.GET['material_id'])
        model = Model.objects.get(id=model_id)
        price = model.calculate_price(material.price_per_kilogram, request.GET.get('scale'))
        return JsonResponse({'price': price})
