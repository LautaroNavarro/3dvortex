from django.urls import path
from prints.views.materials_view import (
    MaterialsView,
    MaterialsByIdView
)
from prints.views.orders_view import (
    OrdersView,
    OrderIpnWrapperView,
    UserOrdersView,
    OrderByIdView,
)


BASE_MATERIAL_URL = 'materials/{}'
BASE_ORDER_URL = 'orders/{}'

urlpatterns = [
    path(BASE_MATERIAL_URL.format(''), MaterialsView.as_view()),
    path(BASE_MATERIAL_URL.format('<int:material_id>'), MaterialsByIdView.as_view()),
    path(BASE_ORDER_URL.format(''), OrdersView.as_view()),
    path(BASE_ORDER_URL.format('<int:order_id>'), OrderByIdView.as_view()),
    path(BASE_ORDER_URL.format('<int:order_id>/ipn'), OrderIpnWrapperView.as_view()),
    path('users/<int:user_id>/orders', UserOrdersView.as_view()),
]
