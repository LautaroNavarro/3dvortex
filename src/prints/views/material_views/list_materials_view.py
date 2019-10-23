from django.http import JsonResponse
from infra.views import BaseView
from prints.models.material import Material
from helpers.view_helpers import require_jwt


class ListMaterialsView(BaseView):

    @require_jwt
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, *args, **kwargs):
        return JsonResponse({
            'materials': [material.serialized for material in Material.objects.all()]
        })
