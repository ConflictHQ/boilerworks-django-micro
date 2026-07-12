# Calliope — Boilerworks Django Micro
<!-- Agent shim for https://github.com/calliopeai/calliope-cli -->

Primary conventions doc: [`bootstrap.md`](bootstrap.md)
Context seed: [`memory.md`](memory.md)

Read both before writing any code.

---

## Project-specific notes

- Django 5 + DRF (Python 3.12+) — API-only REST, JSON responses; PostgreSQL 16.
- API-key auth (`X-API-Key` header, SHA256-hashed) on every endpoint via DRF authentication classes; scope checks via the `require_scope("scope.name")` permission class.
- Every endpoint returns the `ApiResponse` format: `{ok, data, errors}`.
- Never expose integer PKs — use `guid` (UUID) in all responses.
- Soft-delete only: `.soft_delete()`, never `.delete()`.
- Ruff (check + format), max line length 120; tests use pytest-django + DRF `APIClient` with real Postgres.
