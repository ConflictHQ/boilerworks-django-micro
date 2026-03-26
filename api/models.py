import hashlib
import secrets
import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base with UUID external ID and timestamps."""

    guid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Mixin for soft-deleting records."""

    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class ApiKey(TimeStampedModel):
    """API key for service-to-service authentication. Keys are SHA256-hashed before storage."""

    name = models.CharField(max_length=255, help_text="Human-readable label for this key")
    key_hash = models.CharField(max_length=64, unique=True, db_index=True)
    scopes = models.JSONField(default=list, help_text='List of scopes, e.g. ["webhooks.write", "*"]')
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_authenticated(self):
        """DRF compatibility."""
        return True

    def __str__(self):
        return self.name

    def has_scope(self, scope: str) -> bool:
        return "*" in self.scopes or scope in self.scopes

    @classmethod
    def generate(cls, name: str, scopes: list[str] | None = None) -> tuple["ApiKey", str]:
        """Create a new API key. Returns (ApiKey instance, raw key string). Raw key is shown once."""
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        api_key = cls.objects.create(name=name, key_hash=key_hash, scopes=scopes or ["*"])
        return api_key, raw_key

    @classmethod
    def authenticate(cls, raw_key: str) -> "ApiKey | None":
        """Look up an active key by its raw value."""
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        try:
            api_key = cls.objects.get(key_hash=key_hash, is_active=True)
            api_key.last_used_at = timezone.now()
            api_key.save(update_fields=["last_used_at"])
            return api_key
        except cls.DoesNotExist:
            return None
