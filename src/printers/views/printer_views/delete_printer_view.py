from django.http import JsonResponse
from infra.views import BaseView
from infra.request.errors import NotFoundError
from helpers.view_helpers import require_admin
from printers.models.printer import Printer


class DeletePrinterView(BaseView):

    @require_admin
    def validate(self, request, printer_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not Printer.objects.filter(id=printer_id).exists():
            raise NotFoundError('The provided printer id does not exists')

    def run(self, request, printer_id, *args, **kwargs):
        Printer.objects.get(id=printer_id).delete()
        return JsonResponse({'deleted': True})
