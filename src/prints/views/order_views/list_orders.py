from helpers.pagination import PaginatedResponse
from infra.views import PaginatedBaseView
from prints.models.order import Order
from helpers.view_helpers import require_admin


class ListOrdersView(PaginatedBaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

    def run(self, request, page, *args, **kwargs):
        if request.GET.get('status'):
            orders = Order.objects.filter(email__icontains=request.GET.get('email')).order_by('id')
        else:
            orders = Order.objects.all().order_by('id')
        return PaginatedResponse('orders', orders, page)
