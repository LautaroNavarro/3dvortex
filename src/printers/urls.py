from django.urls import path
from printers.views.printers_view import (
    PrinterView,
    PrinterByIdView,
)


urlpatterns = [
    path('', PrinterView.as_view()),
    path('<int:printer_id>', PrinterByIdView.as_view()),
]
