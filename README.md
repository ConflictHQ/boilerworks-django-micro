# Boilerworks Django Micro

Lightweight Django 5 + DRF microservice with API-key auth. No frontend, no sessions, no login flows. Choose this for internal APIs and microservices that need Django's ORM, admin, and migration system.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5 + DRF (Python 3.12+) |
| Auth | API-key (X-API-Key header, SHA256-hashed) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Linter | Ruff |
| Package Manager | uv |

## Quick Start

```bash
docker compose up -d --build
docker compose exec api python manage.py migrate
docker compose exec api python manage.py createsuperuser

# Create an API key via admin
open http://localhost:8002/admin/

# Test the API
curl -H "X-API-Key: <your-key>" http://localhost:8002/api/keys/
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health/` | No | Health check |
| GET | `/api/keys/` | Yes | List API keys |
| POST | `/api/keys/` | Yes | Create API key |
| DELETE | `/api/keys/<guid>/` | Yes | Revoke key |
| POST | `/api/webhooks/` | Yes | Receive webhook |
| GET | `/api/webhooks/events/` | Yes | List events |
| GET | `/api/webhooks/events/<guid>/` | Yes | Get event |
| DELETE | `/api/webhooks/events/<guid>/` | Yes | Soft-delete event |

## Conventions

See [`bootstrap.md`](bootstrap.md) for the full conventions document.

Key patterns:
- `TimeStampedModel` base (UUID guid, timestamps) + `SoftDeleteMixin`
- API-key auth on every endpoint, per-key scopes
- All responses wrapped in `ApiResponse` format: `{ok, data, errors}`
- Tests against real Postgres via DRF `APIClient`

---

Boilerworks is a [CONFLICT](https://weareconflict.com) brand. CONFLICT is a registered trademark of CONFLICT LLC.
