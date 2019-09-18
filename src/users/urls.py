from django.urls import path
from users.views.authenticate import AuthenticateResourceView
from users.views.user import UserResourceView

urlpatterns = [
    path('authenticate/', AuthenticateResourceView.as_view()),
    path('', UserResourceView.as_view()),
]
