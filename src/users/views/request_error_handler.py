from django.http import JsonResponse
from users.views.request_errors import RequestError


def RequestErrorHandler(validation):
    """
    It receives a binded function that can return request errors.
    It returns JsonResponses
    """
    try:
        validation()
    except RequestError as error:
        return JsonResponse(
            {
                'error_message': error.error_message,
            },
            status=error.status_code,
        )
