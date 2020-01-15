from django.urls import path
from users.views.authenticate import AuthenticateResourceView
from users.views.user_view import UserView
from users.views.addresses_view import UserAddressView
urlpatterns = [
    path('authenticate/', AuthenticateResourceView.as_view()),
    path('<int:user_id>/addresses', UserAddressView.as_view()),
    path('', UserView.as_view()),
]
