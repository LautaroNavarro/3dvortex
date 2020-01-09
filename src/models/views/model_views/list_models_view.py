from infra.views import PaginatedBaseView
from models.models.model import Model
from helpers.view_helpers import require_jwt
from helpers.pagination import PaginatedResponse


class ListModelsView(PaginatedBaseView):

    @require_jwt
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, page, *args, **kwargs):
        order_by = 'id'
        if 'newests' in request.GET.keys():
            order_by = '-id'
        query = Model.objects.filter(
            privacy=Model.Privacy.PUBLIC.value,
        ).order_by(order_by)
        return PaginatedResponse('models', query, page)
