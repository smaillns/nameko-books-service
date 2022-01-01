class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class NotFound(HttpError):
    error_code = 'NOT_FOUND'
    status_code = 404


class BadRequest(HttpError):
    error_code = 'BAD_REQUEST'
    status_code = 400