# Claude -- Boilerworks Django Micro

Primary conventions doc: [`bootstrap.md`](bootstrap.md)

Read it before writing any code.

## Stack

- **Backend**: Django 5 + DRF (Python 3.12+)
- **Frontend**: None (API-only)
- **API**: REST (DRF serializers, JSON responses)
- **Auth**: API-key (X-API-Key header, SHA256-hashed)
- **ORM**: Django ORM
- **Database**: PostgreSQL 16
- **Linter**: Ruff (check + format), max line length 120

## Claude-specific notes

- Every endpoint returns `ApiResponse` format: `{ok, data, errors}`.
- Never expose integer PKs — use `guid` (UUID) in all responses.
- API-key auth on every endpoint via DRF authentication classes.
- Scope checks via `require_scope("scope.name")` permission class.
- Soft-delete only: call `.soft_delete()`, never `.delete()`.
- Tests: pytest-django + DRF `APIClient` with real Postgres.
