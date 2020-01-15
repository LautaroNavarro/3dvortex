from helpers.pagination import PaginatedResponse
from infra.views import PaginatedBaseView
from infra.request.errors import NotAuthorizedError
from users.models.user import User
from helpers.view_helpers import require_jwt


class ListUserAddressesView(PaginatedBaseView):

    @require_jwt
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if self.user_payload['id'] != user_id:
            raise NotAuthorizedError('You are not allow to list the addresses for this user')

    def run(self, request, page, user_id, *args, **kwargs):
        user = User.objects.get(id=self.user_payload['id'])
        return PaginatedResponse('addresses', user.addresses.all(), page)
