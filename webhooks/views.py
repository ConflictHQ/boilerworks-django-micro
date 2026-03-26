from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.auth import require_scope
from api.views import api_response

from .models import WebhookEvent
from .serializers import WebhookEventOutSerializer, WebhookPayloadSerializer


class WebhookReceiveView(APIView):
    @method_decorator(ratelimit(key="ip", rate="30/m", block=True))
    def post(self, request):
        """Receive and store a webhook event."""
        serializer = WebhookPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = WebhookEvent.objects.create(
            event=serializer.validated_data["event"],
            source=serializer.validated_data.get("source", ""),
            payload=serializer.validated_data["data"],
        )
        out = WebhookEventOutSerializer(event)
        return api_response(ok=True, data=out.data, http_status=status.HTTP_201_CREATED)


class WebhookListView(APIView):
    def get(self, request):
        """List recent webhook events (max 100)."""
        events = WebhookEvent.objects.all()[:100]
        serializer = WebhookEventOutSerializer(events, many=True)
        return api_response(ok=True, data=serializer.data)


class WebhookDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), require_scope("webhooks.delete")()]
        return super().get_permissions()

    def get(self, request, guid):
        """Get a specific webhook event by GUID."""
        try:
            event = WebhookEvent.objects.get(guid=guid)
        except WebhookEvent.DoesNotExist:
            return api_response(ok=False, errors=[{"detail": "Not found"}], http_status=status.HTTP_404_NOT_FOUND)
        return api_response(ok=True, data=WebhookEventOutSerializer(event).data)

    def delete(self, request, guid):
        """Soft-delete a webhook event. Requires webhooks.delete scope."""
        try:
            event = WebhookEvent.objects.get(guid=guid)
        except WebhookEvent.DoesNotExist:
            return api_response(ok=False, errors=[{"detail": "Not found"}], http_status=status.HTTP_404_NOT_FOUND)

        event.soft_delete()
        return api_response(ok=True, data={"message": "Event deleted"})
