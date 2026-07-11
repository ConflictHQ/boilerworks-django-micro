# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Boilerworks, please report it responsibly.

**Do not open a public issue.**

Instead, email **security@weareconflict.com** with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge your report within 48 hours and aim to release a fix within 7 days for critical issues.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | Yes       |

## Security Best Practices

When deploying Boilerworks Django Micro:

- Set `DJANGO_SECRET_KEY` to a unique, unpredictable value (the app refuses to start in production with the default)
- Set `DJANGO_DEBUG=false` in production
- Restrict `DJANGO_ALLOWED_HOSTS` to your domain(s) only
- Configure `CORS_ALLOWED_ORIGINS` to your domain only, and keep `CORS_ALLOW_ALL_ORIGINS=false`
- Change the default Postgres credentials (`POSTGRES_USER` / `POSTGRES_PASSWORD`)
- Use HTTPS in production
- Never commit `.env` — use `.env.example` as the reference
