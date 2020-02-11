from django.views import View
from models.views.model_views.create_model_view import CreateModelView
from models.views.model_views.list_models_view import ListModelsView
from models.views.model_views.list_user_models import ListUserModelsView
from models.views.model_views.get_model_price import GetModelPrice
from models.views.model_views.get_model_by_id_view import GetModelByIdView


class ModelsView(View):

    def post(self, request, *args, **kwargs):
        view = CreateModelView()
        return view(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = ListModelsView()
        return view(request, *args, **kwargs)


class ModelsByIdView(View):

    def get(self, request, *args, **kwargs):
        view = GetModelByIdView()
        return view(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class UserModelView(View):

    def get(self, request, *args, **kwargs):
        view = ListUserModelsView()
        return view(request, *args, **kwargs)


class ModelsPrice(View):

    def get(self, request, *args, **kwargs):
        view = GetModelPrice()
        return view(request, *args, **kwargs)
