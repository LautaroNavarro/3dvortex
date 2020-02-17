from helpers.pagination import PaginatedResponse
from infra.views import PaginatedBaseView
from prints.models.order import Order
from users.models.user import User
from helpers.view_helpers import require_jwt
from infra.request.errors import (
    NotFoundError,
    ForbiddenError,
)


class ListUserOrdersView(PaginatedBaseView):

    @require_jwt
    def validate(self, request, user_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not User.objects.filter(id=user_id).exists():
            raise NotFoundError('The provided user id does not exists')
        if self.user_payload['access_level'] >= User.Type.ADMIN_USER_TYPE:
            return
        if self.user_payload['id'] != user_id:
            raise ForbiddenError('You are not allow to access this resources')

    def run(self, request, page, user_id, *args, **kwargs):
        orders = Order.objects.filter(
            status__gte=Order.Status.READY_TO_BE_PRINTED.value,
            payment_status=Order.PaymentStatus.PAID.value,
            user_id=user_id,
        ).order_by('id')
        return PaginatedResponse('orders', orders, page)
