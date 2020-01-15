from django.views import View
from users.views.address_views.create_user_address_view import CreateUserAddressView


class UserAddressView(View):

    def post(self, request, *args, **kwargs):
        view = CreateUserAddressView()
        return view(request, *args, **kwargs)
