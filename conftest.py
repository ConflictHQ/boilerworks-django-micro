import hashlib

import pytest
from rest_framework.test import APIClient

from api.models import ApiKey


@pytest.fixture
def raw_api_key():
    return "test-key-abc123"


@pytest.fixture
def api_key(db, raw_api_key):
    key_hash = hashlib.sha256(raw_api_key.encode()).hexdigest()
    return ApiKey.objects.create(name="test-key", key_hash=key_hash, scopes=["*"])


@pytest.fixture
def api_client(api_key, raw_api_key):
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=raw_api_key)
    return client


@pytest.fixture
def anon_client():
    return APIClient()
