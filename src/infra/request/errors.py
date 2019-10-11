
class RequestError(Exception):
    pass


class BadRequestError(RequestError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = args[0] if args else 'Bad request'
        self.status_code = 400


class ForbiddenError(RequestError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = args[0] if args else 'Forbidden'
        self.status_code = 403


class NotAuthorizedError(RequestError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = args[0] if args else 'Not authorized'
        self.status_code = 401


class NotFoundError(RequestError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = args[0] if args else 'Not authorized'
        self.status_code = 404
