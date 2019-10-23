from django.views import View
from prints.views.material_views.create_material_view import CreateMaterialView
from prints.views.material_views.get_material_by_id_view import GetMaterialByIdView


class MaterialsView(View):

    def post(self, request, *args, **kwargs):
        view = CreateMaterialView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pass


class MaterialsByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetMaterialByIdView()
        return view(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
