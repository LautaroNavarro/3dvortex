from enum import Enum
from django.views import View
from users.views.request_error_handler import request_error_handler


class BaseView(View):

    class Method(Enum):
        POST = 'post'
        PUT = 'put'
        GET = 'get'
        PATCH = 'patch'

    def __init__(self, *args, **kwargs):
        setattr(self, self.METHOD, self.wrapper)
        super().__init__(*args, **kwargs)

    def validate(self, request):
        pass

    @request_error_handler
    def wrapper(self, request):
        self.validate(request)
        return self.run(request)
