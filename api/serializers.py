from rest_framework import serializers

from .models import ApiKey


class ApiKeyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    scopes = serializers.ListField(child=serializers.CharField(), required=False, default=["*"])


class ApiKeyOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ["guid", "name", "scopes", "is_active", "last_used_at", "created_at"]


class ApiKeyCreatedSerializer(serializers.Serializer):
    """Response after creating a key — includes the raw key (shown once)."""

    key = serializers.CharField()
    api_key = ApiKeyOutSerializer()
