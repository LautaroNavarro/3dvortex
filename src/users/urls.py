from django.urls import path
from users.views.authenticate import AuthenticateResourceView
from users.views.user_view import UserView

urlpatterns = [
    path('authenticate/', AuthenticateResourceView.as_view()),
    path('', UserView.as_view()),
]
