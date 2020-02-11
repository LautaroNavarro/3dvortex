from django.views import View
from users.views.user_views.create import CreateUserView
from users.views.user_views.list import ListUsersView
from users.views.user_views.delete import DeleteUserView
from users.views.user_views.update import UpdateUserView
from users.views.user_views.get import GetUserByIdView


class UserView(View):

    def post(self, request):
        view = CreateUserView()
        return view(request)

    def get(self, request):
        view = ListUsersView()
        return view(request)


class UserByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetUserByIdView()
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view = DeleteUserView()
        return view(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        view = UpdateUserView()
        return view(request, *args, **kwargs)
