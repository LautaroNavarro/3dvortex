import jsonschema
from infra.request.errors import BadRequestError


def map_json_error_to_request_errors(validate_request_schema):
    """
    Use this decorator to map json validation error to request error
    """
    def wrapper(*args, **kwargs):
        try:
            return validate_request_schema(*args, **kwargs)
        except jsonschema.exceptions.ValidationError as error:
            raise BadRequestError(error.message)
    return wrapper
