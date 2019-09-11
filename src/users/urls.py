from django.urls import path
from users.views.authenticate import AuthenticateView

urlpatterns = [
    path('authenticate/', AuthenticateView.as_view()),
]
