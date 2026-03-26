import hashlib

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import ApiKey

from .models import WebhookEvent


@pytest.fixture
def sample_event(db):
    return WebhookEvent.objects.create(event="order.created", source="shopify", payload={"id": "123", "total": 99.99})


@pytest.mark.django_db
class TestWebhookReceive:
    def test_receive_webhook(self, api_client):
        response = api_client.post(
            reverse("webhook-receive"),
            {"event": "order.created", "source": "shopify", "data": {"id": "456"}},
            format="json",
        )
        assert response.status_code == 201
        assert response.json()["ok"] is True
        event = WebhookEvent.objects.get(event="order.created")
        assert event.payload == {"id": "456"}

    def test_receive_webhook_no_auth(self, anon_client):
        response = anon_client.post(
            reverse("webhook-receive"),
            {"event": "order.created", "data": {}},
            format="json",
        )
        assert response.status_code in (401, 403)

    def test_receive_webhook_invalid_payload(self, api_client):
        response = api_client.post(reverse("webhook-receive"), {"bad": "data"}, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestWebhookList:
    def test_list_events(self, api_client, sample_event):
        response = api_client.get(reverse("webhook-list"))
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1
        assert data[0]["event"] == "order.created"


@pytest.mark.django_db
class TestWebhookDetail:
    def test_get_event(self, api_client, sample_event):
        response = api_client.get(reverse("webhook-detail", kwargs={"guid": sample_event.guid}))
        assert response.status_code == 200
        assert response.json()["data"]["event"] == "order.created"

    def test_get_nonexistent_event(self, api_client):
        import uuid

        response = api_client.get(reverse("webhook-detail", kwargs={"guid": uuid.uuid4()}))
        assert response.status_code == 404

    def test_delete_event_with_scope(self, api_client, sample_event):
        """Wildcard scope should allow deletion."""
        response = api_client.delete(reverse("webhook-detail", kwargs={"guid": sample_event.guid}))
        assert response.status_code == 200
        sample_event.refresh_from_db()
        assert sample_event.is_deleted

    def test_delete_event_without_scope(self, sample_event):
        """Key without webhooks.delete scope should be denied."""
        raw = "limited-key"
        key_hash = hashlib.sha256(raw.encode()).hexdigest()
        ApiKey.objects.create(name="limited", key_hash=key_hash, scopes=["webhooks.read"])
        client = APIClient()
        client.credentials(HTTP_X_API_KEY=raw)
        response = client.delete(reverse("webhook-detail", kwargs={"guid": sample_event.guid}))
        assert response.status_code == 403

    def test_soft_delete_excludes_from_active(self, api_client, sample_event):
        sample_event.soft_delete()
        response = api_client.get(reverse("webhook-list"))
        guids = [e["guid"] for e in response.json()["data"]]
        assert str(sample_event.guid) not in guids
