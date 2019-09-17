from infra.request.handler import request_error_handler


class BaseView():

    @request_error_handler
    def __call__(self, request):
        self.validate(request)
        return self.run(request)

    def validate(self, request):
        pass
