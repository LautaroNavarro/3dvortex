from django.views import View
from users.views.address_views.create_user_address_view import CreateUserAddressView
from users.views.address_views.list_user_addresses_view import ListUserAddressesView


class UserAddressView(View):

    def post(self, request, *args, **kwargs):
        view = CreateUserAddressView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListUserAddressesView()
        return view(request, *args, **kwargs)
