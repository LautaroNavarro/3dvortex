from django.views import View
from models.views.model_views.create_model_view import CreateModelView


class ModelsView(View):

    def post(self, request, *args, **kwargs):
        view = CreateModelView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pass


class ModelsByIdView(View):

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
