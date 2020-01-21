from infra.views import PaginatedBaseView
from models.models.model import Model
from helpers.pagination import PaginatedResponse
from helpers.view_helpers import require_jwt
from users.models.user import User
from infra.request.errors import (
    BadRequestError,
)


class ListUserModelsView(PaginatedBaseView):

    @require_jwt
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not User.objects.filter(id=user_id).exists():
            raise BadRequestError('The provided user does not exist.')

    def run(self, request, page, user_id, *args, **kwargs):
        filters = {'user_id': user_id}
        if self.user_payload['access_level'] < User.Type.ADMIN_USER_TYPE and self.user_payload['id'] != user_id:
            filters = {'privacy': Model.Privacy.PUBLIC.value}
        query = Model.objects.filter(**filters).order_by('id')
        return PaginatedResponse('models', query, page)
