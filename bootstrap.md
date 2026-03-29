# Boilerworks Django Micro -- Bootstrap

Primary conventions document. All agent shims point here.

---

## What's Already Built

| Layer | What's there |
|---|---|
| Auth | API-key auth (SHA256-hashed, X-API-Key header), per-key scopes |
| Data | Postgres 16, `TimeStampedModel` base (UUID guid, timestamps), `SoftDeleteMixin` |
| API | DRF REST endpoints returning `ApiResponse` (`{ok, data, errors}`) |
| Admin | Django Admin for API key management (key shown once on creation) |
| Infra | Docker Compose: api, postgres, redis |
| CI | GitHub Actions: lint (Ruff) + tests (Postgres service) |
| Example | Webhook receiver (receive, list, detail, soft-delete) |

---

## App Structure

| App | Purpose |
|---|---|
| `config` | Django settings, URLs |
| `api` | ApiKey model, auth middleware, key management endpoints |
| `webhooks` | Webhook receiver (example domain) |

---

## Conventions

### Models

```python
from api.models import TimeStampedModel, SoftDeleteMixin, ActiveManager

class MyModel(TimeStampedModel, SoftDeleteMixin):
    name = models.CharField(max_length=255)

    objects = ActiveManager()      # excludes soft-deleted
    all_objects = models.Manager() # includes everything
```

Use `guid` (UUID) in API responses. Never expose integer PKs.

### API Responses

All endpoints return:
```json
{"ok": true, "data": {...}, "errors": null}
```

Use `api_response()` helper from `api.views`.

### Auth

Every endpoint requires API key via `X-API-Key` header. Keys are SHA256-hashed before storage.

Scope checks:
```python
from api.auth import require_scope

class MyView(APIView):
    permission_classes = [require_scope("my.scope")]
```

### Tests

pytest-django + DRF `APIClient` with real Postgres.

```python
def test_my_endpoint(api_client):
    response = api_client.post("/api/my-endpoint/", {"data": "value"}, format="json")
    assert response.status_code == 200
    assert response.json()["ok"] is True
```

---

## Ports (local Docker)

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Admin | http://localhost:8000/admin/ |
| Health | http://localhost:8000/health/ |
| Postgres | localhost:5432 |
| Redis | localhost:6379 |

---

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health/` | No | Health check |
| GET | `/api/keys/` | Yes | List API keys |
| POST | `/api/keys/` | Yes | Create API key (raw key shown once) |
| DELETE | `/api/keys/<guid>/` | Yes | Revoke API key |
| POST | `/api/webhooks/` | Yes | Receive webhook event |
| GET | `/api/webhooks/events/` | Yes | List webhook events |
| GET | `/api/webhooks/events/<guid>/` | Yes | Get webhook event |
| DELETE | `/api/webhooks/events/<guid>/` | Yes | Soft-delete event (requires webhooks.delete scope) |

---

## Commands

```bash
make up         # Start the stack
make build      # Build and start
make down       # Stop
make migrate    # Run migrations
make test       # Run tests
make lint       # Run Ruff
```
