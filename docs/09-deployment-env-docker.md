# Deployment, Docker, and EasyPanel

## Required Repo Shape

```text
khafeefa-store/
  frontend/
  backend/
  sheets/
  docs/
  docker-compose.yml
  README.md
```

## Frontend Dockerfile

Requirements:

- Multi-stage build.
- Use Node LTS.
- Build Next.js app.
- Run as non-root user.
- Expose `3000`.

Expected command:

```bash
npm run build
npm run start
```

## Backend Dockerfile

Requirements:

- Python 3.12 slim.
- Install dependencies through `uv` or `pip`.
- Run Alembic migration before server start.
- Expose `8000`.

Expected command:

```bash
alembic upgrade head && gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Local Docker Compose

Include:

- `frontend`
- `backend`
- `postgres`

Local Postgres may use:

```env
POSTGRES_DB=khafeefa
POSTGRES_USER=khafeefa
POSTGRES_PASSWORD=khafeefa
```

Do not commit real production secrets.

## EasyPanel Services

Frontend:

- Domain: `getkhafeefa.shop`
- Port: `3000`
- Env from `frontend/.env.example`.

Backend:

- Domain: `api.getkhafeefa.shop`
- Port: `8000`
- Env from `backend/.env.example`.
- Database internal host: `khafeefa_database`.
- Database name: `getkhafeefa`.
- Database URL: `postgres://getkhafeefa:getkhafeefa@khafeefa_database:5432/getkhafeefa?sslmode=disable`

Database:

- Already installed by owner.
- Store the database URL in backend environment variables only.

## DNS

Point:

- `getkhafeefa.shop` to frontend service.
- `api.getkhafeefa.shop` to backend service.

Use HTTPS certificates in EasyPanel.

## Production Security

- CORS only allows frontend domain.
- API rate limit order endpoint.
- Do not expose docs/OpenAPI publicly in production unless protected or acceptable.
- Validate request origin and content type.
- Log enough for debugging, but do not log full access tokens.
- Hash PII before sending CAPI.

## CI Suggestions

GitHub Actions:

- Frontend: typecheck, lint, build.
- Backend: ruff, mypy optional, pytest, alembic migration check.
- Docker build for both images.

