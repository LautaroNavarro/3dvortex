from django.views import View
from models.views.model_views.create_model_view import CreateModelView
from models.views.model_views.list_models_view import ListModelsView


class ModelsView(View):

    def post(self, request, *args, **kwargs):
        view = CreateModelView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListModelsView()
        return view(request, *args, **kwargs)


class ModelsByIdView(View):

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
