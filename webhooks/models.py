from django.db import models

from api.models import ActiveManager, SoftDeleteMixin, TimeStampedModel


class WebhookEvent(TimeStampedModel, SoftDeleteMixin):
    """Stores received webhook events for processing and audit."""

    event = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=255, blank=True, default="")
    payload = models.JSONField(default=dict)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event} ({self.guid})"
