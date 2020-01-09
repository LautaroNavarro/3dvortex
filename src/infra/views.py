import json
from jsonschema import validate as validate_request
from infra.request.handler import (
    request_error_handler,
    json_error_handler,
)
from infra.request.mapping import map_json_error_to_request_errors
from infra.request.errors import BadRequestError


class BaseView():

    content_type = None

    schema = None

    required_body = False

    @json_error_handler
    @request_error_handler
    def __call__(self, request, *args, **kwargs):
        self.validate(request, *args, **kwargs)
        return self.run(request, *args, **kwargs)

    def validate(self, request, *args, **kwargs):
        self.validate_request_content_type(request)
        self.validate_request_schema(request)

    @map_json_error_to_request_errors
    def validate_request_schema(self, request):
        if self.required_body and not request.body:
            raise BadRequestError('You must pass a body')
        if self.schema:
            request_params = json.loads(request.body)
            validate_request(instance=request_params, schema=self.schema)

    def validate_request_content_type(self, request):
        if self.content_type:
            if not request.content_type == self.content_type:
                raise BadRequestError('Content type must be {}.'.format(self.content_type))


class PaginatedBaseView(BaseView):

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if request.GET.get('page') and request.GET.get('page') < 1:
            raise BadRequestError('Page number must be positive')

    @json_error_handler
    @request_error_handler
    def __call__(self, request, *args, **kwargs):
        self.validate(request, *args, **kwargs)
        return self.run(request, int(request.GET.get('page', 1)), *args, **kwargs)
