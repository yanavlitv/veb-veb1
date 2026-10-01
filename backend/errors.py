def error_response(message, status, fields=None):
    error = {
        "message": message
    }

    if fields is not None:
        error["fields"] = fields

    return {
        "error": error
    }, status