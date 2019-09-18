from json.decoder import JSONDecodeError
from django.http import JsonResponse
from infra.request.errors import RequestError


def json_error_handler(run):
    """
    Use this decorator to catch json errors
    """
    def wrapper(*args, **kwargs):
        try:
            return run(*args, **kwargs)
        except JSONDecodeError:
            return JsonResponse(
                {
                    'error_message': 'Not a json body',
                },
                status=400,
            )
    return wrapper


def request_error_handler(run):
    """
    Use this decorator to catch request errors
    """
    def wrapper(*args, **kwargs):
        try:
            return run(*args, **kwargs)
        except RequestError as error:
            return JsonResponse(
                {
                    'error_message': error.error_message,
                },
                status=error.status_code,
            )
    return wrapper
