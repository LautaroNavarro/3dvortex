from infra.request.handler import request_error_handler
from infra.request.errors import BadRequestError
from django.http import JsonResponse


class TestRequestErrorHandler():

    def test_catch_bad_request_error_and_return_json_response(self):
        @request_error_handler
        def get_think():
            raise BadRequestError('Invalid field error')
            return 'think'

        json_response = get_think()
        assert isinstance(json_response, JsonResponse)
        assert json_response.status_code == 400
        assert json_response.content == b'{"error_message": "Invalid field error"}'
