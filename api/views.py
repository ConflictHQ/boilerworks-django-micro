from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ApiKey
from .serializers import ApiKeyCreatedSerializer, ApiKeyCreateSerializer, ApiKeyOutSerializer


def api_response(ok: bool, data=None, errors=None, http_status=200):
    return Response({"ok": ok, "data": data, "errors": errors}, status=http_status)


class ApiKeyListCreateView(APIView):
    def get(self, request):
        """List all active API keys."""
        keys = ApiKey.objects.filter(is_active=True)
        serializer = ApiKeyOutSerializer(keys, many=True)
        return api_response(ok=True, data=serializer.data)

    @method_decorator(ratelimit(key="ip", rate="10/m", block=True))
    def post(self, request):
        """Create a new API key. The raw key is returned once."""
        serializer = ApiKeyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_key, raw_key = ApiKey.generate(
            name=serializer.validated_data["name"],
            scopes=serializer.validated_data.get("scopes", ["*"]),
        )
        out = ApiKeyCreatedSerializer({"key": raw_key, "api_key": api_key})
        return api_response(ok=True, data=out.data, http_status=status.HTTP_201_CREATED)


class ApiKeyRevokeView(APIView):
    def delete(self, request, guid):
        """Revoke (deactivate) an API key by GUID."""
        try:
            api_key = ApiKey.objects.get(guid=guid, is_active=True)
        except ApiKey.DoesNotExist:
            return api_response(
                ok=False, errors=[{"detail": "API key not found"}], http_status=status.HTTP_404_NOT_FOUND
            )

        api_key.is_active = False
        api_key.save(update_fields=["is_active", "updated_at"])
        return api_response(ok=True, data={"message": f"Key '{api_key.name}' revoked"})
