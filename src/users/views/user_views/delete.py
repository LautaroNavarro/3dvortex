from django.http import JsonResponse
from infra.request.errors import (
    BadRequestError,
    NotFoundError,
)
from infra.views import BaseView
from users.models.user import User
from helpers.view_helpers import require_admin


class DeleteUserView(BaseView):

    @require_admin
    def validate(self, request, user_id, *args, **kwargs):
        if not request.content_type == 'application/json':
            raise BadRequestError('Content type must be application/json.')
        if not User.objects.filter(id=user_id).exists():
            raise NotFoundError('The provided user id does not exists')

    def run(self, request, user_id, *args, **kwargs):
        User.objects.filter(id=user_id).delete()
        return JsonResponse({'deleted': True})
