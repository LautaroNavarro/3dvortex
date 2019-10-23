from django.views import View
from prints.views.material_views.create_material_view import CreateMaterialView
from prints.views.material_views.get_material_by_id_view import GetMaterialByIdView
from prints.views.material_views.list_materials_view import ListMaterialsView
from prints.views.material_views.update_material_view import UpdateMaterialView
from prints.views.material_views.delete_material_view import DeleteMaterialView


class MaterialsView(View):

    def post(self, request, *args, **kwargs):
        view = CreateMaterialView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListMaterialsView()
        return view(request, *args, **kwargs)


class MaterialsByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetMaterialByIdView()
        return view(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        view = UpdateMaterialView()
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view = DeleteMaterialView()
        return view(request, *args, **kwargs)
