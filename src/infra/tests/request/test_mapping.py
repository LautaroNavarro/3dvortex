import pytest
import jsonschema
from infra.request.mapping import map_json_error_to_request_errors
from infra.request.errors import BadRequestError


class TestRequestErrorHandler():

    def test_catch_bad_request_error_and_return_json_response(self):
        @map_json_error_to_request_errors
        def get_think():
            raise jsonschema.exceptions.ValidationError('Invalid field error')
        print('\n\n\n\n\n\n\n\n\n')
        with pytest.raises(BadRequestError) as e:
            get_think()
        assert e.value.args[0] == 'Invalid field error'
