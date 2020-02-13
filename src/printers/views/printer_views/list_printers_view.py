from infra.views import PaginatedBaseView
from helpers.view_helpers import require_admin
from helpers.pagination import PaginatedResponse
from printers.models.printer import Printer


class ListPrintersView(PaginatedBaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

    def run(self, request, page, *args, **kwargs):
        filters = {}
        if request.GET.get('name'):
            filters['name__icontains'] = request.GET.get('name')
        printers = Printer.objects.filter(**filters).order_by('id')
        return PaginatedResponse('printers', printers, page)
