from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from .models import ApiKey


class ApiKeyAuthentication(BaseAuthentication):
    """Authenticate requests via X-API-Key header. Key is SHA256-hashed and looked up."""

    def authenticate(self, request):
        raw_key = request.META.get("HTTP_X_API_KEY")
        if not raw_key:
            return None

        api_key = ApiKey.authenticate(raw_key)
        if api_key is None:
            raise AuthenticationFailed("Invalid or inactive API key.")

        return (api_key, None)


class HasScope(BasePermission):
    """Check that the authenticated API key has the required scope."""

    def __init__(self, scope: str):
        self.scope = scope

    def has_permission(self, request, view):
        api_key = request.user
        if not isinstance(api_key, ApiKey):
            return False
        return api_key.has_scope(self.scope)


def require_scope(scope: str):
    """Factory for creating HasScope permission instances. Use in view permission_classes."""

    class ScopePermission(BasePermission):
        def has_permission(self, request, view):
            api_key = request.user
            if not isinstance(api_key, ApiKey):
                return False
            return api_key.has_scope(scope)

    ScopePermission.__name__ = f"HasScope_{scope.replace('.', '_')}"
    return ScopePermission
