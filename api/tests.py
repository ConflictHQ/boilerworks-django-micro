import hashlib

import pytest
from django.urls import reverse

from .models import ApiKey


@pytest.mark.django_db
class TestApiKeyModel:
    def test_generate_creates_key(self):
        api_key, raw_key = ApiKey.generate(name="test", scopes=["*"])
        assert api_key.key_hash == hashlib.sha256(raw_key.encode()).hexdigest()
        assert api_key.is_active is True
        assert api_key.guid is not None

    def test_authenticate_valid_key(self):
        _, raw_key = ApiKey.generate(name="test")
        result = ApiKey.authenticate(raw_key)
        assert result is not None
        assert result.last_used_at is not None

    def test_authenticate_invalid_key(self):
        result = ApiKey.authenticate("nonexistent-key")
        assert result is None

    def test_authenticate_inactive_key(self):
        api_key, raw_key = ApiKey.generate(name="test")
        api_key.is_active = False
        api_key.save()
        assert ApiKey.authenticate(raw_key) is None

    def test_has_scope_wildcard(self):
        api_key, _ = ApiKey.generate(name="test", scopes=["*"])
        assert api_key.has_scope("anything") is True

    def test_has_scope_specific(self):
        api_key, _ = ApiKey.generate(name="test", scopes=["webhooks.read"])
        assert api_key.has_scope("webhooks.read") is True
        assert api_key.has_scope("webhooks.write") is False


@pytest.mark.django_db
class TestApiKeyEndpoints:
    def test_list_keys(self, api_client, api_key):
        response = api_client.get(reverse("api-keys"))
        assert response.status_code == 200
        assert response.json()["ok"] is True
        assert len(response.json()["data"]) >= 1

    def test_create_key(self, api_client):
        response = api_client.post(
            reverse("api-keys"),
            {"name": "new-key", "scopes": ["webhooks.read"]},
            format="json",
        )
        assert response.status_code == 201
        data = response.json()["data"]
        assert "key" in data
        assert data["api_key"]["name"] == "new-key"
        assert ApiKey.objects.filter(name="new-key").exists()

    def test_revoke_key(self, api_client):
        new_key, _ = ApiKey.generate(name="to-revoke")
        response = api_client.delete(reverse("api-key-revoke", kwargs={"guid": new_key.guid}))
        assert response.status_code == 200
        new_key.refresh_from_db()
        assert new_key.is_active is False

    def test_revoke_nonexistent_key(self, api_client):
        import uuid

        response = api_client.delete(reverse("api-key-revoke", kwargs={"guid": uuid.uuid4()}))
        assert response.status_code == 404

    def test_no_auth_returns_403(self, anon_client):
        response = anon_client.get(reverse("api-keys"))
        assert response.status_code == 403

    def test_invalid_key_returns_403(self):
        """DRF coerces AuthenticationFailed to 403 when no WWW-Authenticate header is set."""
        from rest_framework.test import APIClient

        client = APIClient()
        client.credentials(HTTP_X_API_KEY="bad-key")
        response = client.get(reverse("api-keys"))
        assert response.status_code == 403


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_returns_ok(self, anon_client):
        response = anon_client.get(reverse("health"))
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
