from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Custom exception handler wrapping errors in the ApiResponse format."""
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(response.data, dict):
            if "detail" in response.data:
                errors = [{"detail": str(response.data["detail"])}]
            else:
                errors = [
                    {"field": k, "messages": v if isinstance(v, list) else [str(v)]} for k, v in response.data.items()
                ]
        else:
            errors = [{"detail": str(response.data)}]
        response.data = {"ok": False, "data": None, "errors": errors}
    return response
