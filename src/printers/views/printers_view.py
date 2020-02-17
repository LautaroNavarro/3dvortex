from django.views import View
from printers.views.printer_views.create_printer_view import CreatePrinterView
from printers.views.printer_views.list_printers_view import ListPrintersView
from printers.views.printer_views.delete_printer_view import DeletePrinterView
from printers.views.printer_views.get_printer_view import GetPrinterView
from printers.views.printer_views.update_printer_view import UpdatePrinterView


class PrinterView(View):

    def post(self, request, *args, **kwargs):
        view = CreatePrinterView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListPrintersView()
        return view(request, *args, **kwargs)


class PrinterByIdView(View):

    def delete(self, request, *args, **kwargs):
        view = DeletePrinterView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = GetPrinterView()
        return view(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        view = UpdatePrinterView()
        return view(request, *args, **kwargs)
