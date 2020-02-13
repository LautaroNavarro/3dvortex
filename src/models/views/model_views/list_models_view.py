from infra.views import PaginatedBaseView
from models.models.model import Model
from users.models.user import User
from helpers.pagination import PaginatedResponse
from helpers.view_helpers import optional_jwt


class ListModelsView(PaginatedBaseView):

    @optional_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

    def run(self, request, page, *args, **kwargs):
        order_by = []
        filters = {'privacy': Model.Privacy.PUBLIC.value}
        if (
            hasattr(self, 'user_payload') and
            self.user_payload.get('access_level') >= User.Type.ADMIN_USER_TYPE
        ):
            filters = {}
        if 'name' in request.GET.keys():
            filters['name__icontains'] = request.GET.get('name')
        if 'newests' in request.GET.keys():
            order_by.append('-id')
        if 'most_printed' in request.GET.keys():
            order_by.append('-printed_quantity')
        if len(order_by) == 0:
            order_by = ['id']
        query = Model.objects.filter(**filters).order_by(*order_by)
        return PaginatedResponse('models', query, page)
