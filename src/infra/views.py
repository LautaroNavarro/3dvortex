from infra.request.handler import (
    request_error_handler,
    json_error_handler,
)


class BaseView():

    @json_error_handler
    @request_error_handler
    def __call__(self, request, *args, **kwargs):
        self.validate(request, *args, **kwargs)
        return self.run(request, *args, **kwargs)

    def validate(self, request, *args, **kwargs):
        pass
