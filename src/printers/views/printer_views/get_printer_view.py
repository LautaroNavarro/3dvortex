from infra.views import BaseView
from helpers.view_helpers import require_admin
from infra.request.errors import NotFoundError
from django.http import JsonResponse
from printers.models.printer import Printer


class GetPrinterView(BaseView):

    @require_admin
    def validate(self, request, printer_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not Printer.objects.filter(id=printer_id).exists():
            raise NotFoundError('The requested printer does not exists.')

    def run(self, request, printer_id, *args, **kwargs):
        return JsonResponse(Printer.objects.get(id=printer_id).serialized)
