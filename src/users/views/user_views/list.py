from helpers.pagination import PaginatedResponse
from infra.views import PaginatedBaseView
from users.models.user import User
from helpers.view_helpers import require_admin


class ListUsersView(PaginatedBaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        pass

    def run(self, request, page, *args, **kwargs):
        if request.GET.get('email'):
            users = User.objects.filter(email__contains=request.GET.get('email'))
        else:
            users = User.objects.all()
        return PaginatedResponse('users', users, page)
