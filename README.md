# AI Tax Compliance System

<<<<<<< HEAD
This repository currently contains Phases 1-5 of the requested implementation:

- monorepo structure
- backend core and models
- service layer
- Celery worker pipeline
- FastAPI API routes

Frontend, deployment, migrations, and tests are intentionally deferred to later phases.
=======
A production-oriented GST compliance validation and reconciliation platform for CA firms and SMEs in India.

## Start here

For complete setup, testing, and hosting instructions for both the backend and frontend, use:

- `docs/setup-and-deployment.md`

That guide includes:

- exact local setup steps with Docker + manual app processes
- exact full Docker Compose startup steps
- migration and seed instructions
- API and frontend smoke-test steps
- hosted deployment steps for Render, Upstash, Cloudflare R2/AWS S3, and Vercel
- common failure cases and fixes

## Repository layout

```text
backend/   FastAPI app, Celery worker, Alembic migrations, tests
frontend/  React/Vite application
infra/     infrastructure artifacts
docs/      architecture and setup/deployment documentation
scripts/   operational helpers and seed scripts
```

## Quick local start

```bash
cp .env.example .env
docker-compose -f docker-compose.db.yml up -d
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cd backend && alembic upgrade head
cd backend && PYTHONPATH=. python ../scripts/seed_demo_data.py
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd backend && source .venv/bin/activate && celery -A app.workers.tasks worker --loglevel=info
cd frontend && npm install && npm run dev -- --host 0.0.0.0
```

Before testing uploads, start MinIO and create the `compliance-data` bucket as described in `docs/setup-and-deployment.md`.

## Quick hosted target

- Backend API: Render Web Service
- Worker: Render Background Worker
- Database: Render PostgreSQL
- Redis: Upstash Redis
- Object storage: Cloudflare R2 or AWS S3
- Frontend: Vercel

Use `infra/render.yaml` as the starting Render artifact and `docs/setup-and-deployment.md` for the full deployment sequence and required environment variables.
