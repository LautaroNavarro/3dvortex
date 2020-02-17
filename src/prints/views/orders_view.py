from django.views import View
from prints.views.order_views.create_order_view import CreateOrderView
from prints.views.order_views.order_ip_view import OrderIpnView
from prints.views.order_views.list_orders import ListOrdersView
from prints.views.order_views.list_user_order import ListUserOrdersView
from prints.views.order_views.update_order_view import UpdateOrderView


class OrdersView(View):

    def post(self, request, *args, **kwargs):
        view = CreateOrderView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListOrdersView()
        return view(request, *args, **kwargs)


class OrderByIdView(View):

    def get(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        view = UpdateOrderView()
        return view(request, *args, **kwargs)


class OrderIpnWrapperView(View):

    def post(self, request, *args, **kwargs):
        view = OrderIpnView()
        return view(request, *args, **kwargs)


class UserOrdersView(View):

    def get(self, request, *args, **kwargs):
        view = ListUserOrdersView()
        return view(request, *args, **kwargs)
