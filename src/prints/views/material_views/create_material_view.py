from infra.views import BaseView
from helpers.view_helpers import require_admin


class CreateMaterialView(BaseView):

    @require_admin
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        # to be implemented

    def run(self, request, *args, **kwargs):
        pass
        # to be implemented
