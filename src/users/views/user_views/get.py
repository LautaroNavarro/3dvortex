from django.http import JsonResponse
from infra.request.errors import NotFoundError
from infra.views import BaseView
from users.models.user import User
from helpers.view_helpers import require_admin


class GetUserByIdView(BaseView):

    @require_admin
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, user_id, *args, **kwargs)
        if not User.objects.filter(id=user_id).exists():
            raise NotFoundError('User does not exists')

    def run(self, request, user_id, *args, **kwargs):
        return JsonResponse(User.objects.get(id=user_id).serialized)
