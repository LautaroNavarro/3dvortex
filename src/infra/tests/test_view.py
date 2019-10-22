import json
import pytest
import mock
from infra.views import BaseView
from infra.request.errors import BadRequestError


class TestBaseView:

    class TestValidateRequestContentTypeMethod:

        def test_not_raise_error_if_not_setted_content_type(self):
            view = BaseView()
            request = mock.Mock()
            view.validate_request_content_type(request)

        def test_not_raise_error_if_correct_content_type(self):
            view = BaseView()
            view.content_type = 'application/json'
            request = mock.Mock()
            request.content_type = 'application/json'
            view.validate_request_content_type(request)

        def test_raise_error_if_not_correct_content_type(self):
            view = BaseView()
            view.content_type = 'application/json'
            request = mock.Mock()
            request.content_type = 'some/content_type'
            with pytest.raises(BadRequestError):
                view.validate_request_content_type(request)

    class TestValidateRequestSchema:

        def test_not_raise_errr_if_not_required_body_and_no_body(self):
            view = BaseView()
            view.required_body = False
            request = mock.Mock()
            request.body = None
            view.validate_request_schema(request)

        def test_raise_error_if_required_body_and_no_body(self):
            view = BaseView()
            view.required_body = True
            request = mock.Mock()
            request.body = None
            with pytest.raises(BadRequestError):
                view.validate_request_schema(request)

        def test_not_it_do_not_validate_schema_if_not_requested_schema(self):
            view = BaseView()
            view.schema = None
            request = mock.Mock()
            request.body = {}
            view.validate_request_schema(request)

        def test_it_validate_schema_if_requested_schema_invalid_schema(self):
            view = BaseView()
            view.schema = {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                },
                "additionalProperties": False,
            }
            request = mock.Mock()
            request.body = json.dumps({'name': 1})
            with pytest.raises(BadRequestError):
                view.validate_request_schema(request)

        def test_it_validate_schema_if_requested_schema_valid_schema(self):
            view = BaseView()
            view.schema = {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                },
                "additionalProperties": False,
            }
            request = mock.Mock()
            request.body = json.dumps({'name': '1'})
            view.validate_request_schema(request)
