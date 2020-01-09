from infra.views import PaginatedBaseView
from models.models.model import Model
from helpers.view_helpers import require_jwt
from helpers.pagination import PaginatedResponse


class ListModelsView(PaginatedBaseView):

    @require_jwt
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, page, *args, **kwargs):
        return PaginatedResponse('models', Model.objects.filter(
            privacy=Model.Privacy.PUBLIC.value,
        ), page)
