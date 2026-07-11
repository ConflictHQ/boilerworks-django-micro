# Boilerworks Memory

This file is the **AI context seed** for the Boilerworks Django Micro template. It captures decisions, constraints, and non-obvious facts that are not derivable from reading a single file.

For conventions and patterns, see [`bootstrap.md`](bootstrap.md).

---

## Template purpose

API-only Django microservice template: Django 5 + DRF, Python 3.12+, no frontend. Auth is API-key based (`X-API-Key` header, SHA256-hashed, per-key scopes). Ships with a webhook receiver as the example domain.

---

## What's already built

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

## Key decisions

| Decision | Why |
|---|---|
| API-key auth, not sessions/OIDC | Machine-to-machine microservice; keys are SHA256-hashed before storage and shown raw only once on creation |
| `ApiResponse` envelope on every endpoint | Uniform `{ok, data, errors}` shape via the `api_response()` helper in `api.views` |
| `guid` (UUID) as external identifier | Integer PKs are never exposed in API responses |
| Soft deletes only | Call `.soft_delete()`, never `.delete()`; `objects = ActiveManager()` excludes soft-deleted, `all_objects` includes everything |
| Scope checks via permission class | `permission_classes = [require_scope("my.scope")]` from `api.auth` |

---

## Things that bite newcomers

- **Never call `.delete()`** on business objects — use `.soft_delete()`.
- **Never expose integer PKs** — always `guid`.
- **Every endpoint requires an API key** — the raw key appears once at creation and is never retrievable again.
- **Tests run against real Postgres** (pytest-django + DRF `APIClient`), not SQLite.
- **Ruff line length is 120** (check + format).
