from django.http import JsonResponse
from infra.request.errors import NotFoundError
from infra.views import BaseView
from prints.models.material import Material
from helpers.view_helpers import require_jwt


class GetMaterialByIdView(BaseView):

    @require_jwt
    def validate(self, request, material_id, *args, **kwargs):
        if not Material.objects.filter(id=material_id).exists():
            raise NotFoundError('The provided material id does not exists')

    def run(self, request, material_id, *args, **kwargs):
        return JsonResponse(Material.objects.get(id=material_id).serialized)
