from django.views import View
from users.views.user_views.create import CreateUserView


class UserView(View):

    def post(self, request):
        view = CreateUserView()
        return view(request)
