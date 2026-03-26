from rest_framework import serializers

from .models import WebhookEvent


class WebhookPayloadSerializer(serializers.Serializer):
    event = serializers.CharField(max_length=255)
    source = serializers.CharField(max_length=255, required=False, default="")
    data = serializers.JSONField()


class WebhookEventOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ["guid", "event", "source", "payload", "created_at"]
