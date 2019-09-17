
class RequestError(Exception):
    pass


class BadRequestError(RequestError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = args[0] if args[0] else 'Bad request'
        self.status_code = 400
