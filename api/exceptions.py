from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Custom exception handler wrapping errors in the ApiResponse format."""
    response = exception_handler(exc, context)
    if response is not None:
        detail = response.data.get("detail", str(response.data))
        response.data = {
            "ok": False,
            "data": None,
            "errors": [{"detail": detail}] if isinstance(detail, str) else [{"detail": str(detail)}],
        }
    return response
