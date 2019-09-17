from django.urls import path
from users.views.authenticate import AuthenticateResourceView

urlpatterns = [
    path('authenticate/', AuthenticateResourceView.as_view()),
]
