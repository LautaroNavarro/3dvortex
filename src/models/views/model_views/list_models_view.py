from infra.views import PaginatedBaseView
from models.models.model import Model
from helpers.pagination import PaginatedResponse


class ListModelsView(PaginatedBaseView):

    def run(self, request, page, *args, **kwargs):
        order_by = []
        filters = {'privacy': Model.Privacy.PUBLIC.value}
        if 'newests' in request.GET.keys():
            order_by.append('-id')
        if 'most_printed' in request.GET.keys():
            order_by.append('-printed_quantity')
        if len(order_by) == 0:
            order_by = ['id']
        query = Model.objects.filter(**filters).order_by(*order_by)
        return PaginatedResponse('models', query, page)
