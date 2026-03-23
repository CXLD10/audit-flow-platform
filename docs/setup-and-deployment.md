# Setup and Deployment Guide

This guide gives exact, reproducible steps to run the project in two ways:

1. **Locally for testing**
2. **Hosted deployment matching the Phase 1 architecture**

Use this file when you want to validate the backend and frontend together, exercise the worker pipeline, or deploy the stack to managed services.

---

## 1. What you are starting

The application has five runtime parts:

1. **PostgreSQL**: stores tenants, users, clients, batches, invoices, validation errors, reconciliation results, and audit records.
2. **Redis**: acts as the Celery broker/result backend and stores batch progress snapshots.
3. **S3-compatible object storage**: stores uploaded raw files and exported artifacts. Local development uses **MinIO**.
4. **FastAPI backend**: serves the REST API at `/api/v1` and `/health`.
5. **Celery worker**: processes uploaded batches asynchronously.
6. **React frontend**: talks to the backend API and provides login, upload, progress, validation, reconciliation, audit, and export pages.

For a full end-to-end test, all of these must be available at the same time.

---

## 2. Prerequisites

### Local machine requirements

Install the following before starting:

- **Python 3.11**
- **Node.js 20** and **npm**
- **Docker** and **Docker Compose**
- Optional but useful: **psql**, **curl**, and a PostgreSQL GUI

### Ports used locally

Make sure these ports are free:

- `5432` → PostgreSQL
- `6379` → Redis
- `8000` → FastAPI backend
- `9000` → MinIO S3 API
- `9001` → MinIO console
- `5173` → Vite frontend

---

## 3. Environment file

Create the runtime environment file once at the repo root:

```bash
cp .env.example .env
```

For local development, keep or confirm these values inside `.env`:

```env
DATABASE_URL=postgresql://dev:dev@localhost:5432/compliance
REDIS_URL=redis://localhost:6379/0
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=compliance-data
JWT_SECRET=replace-with-a-random-64-character-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GSTN_API_KEY=replace-with-gstn-api-key
GSTN_API_BASE_URL=https://gstn.example.com/api
GSTN_CACHE_TTL=86400
LLM_API_KEY=
APP_ENV=local
LOG_LEVEL=DEBUG
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Important notes

- `S3_BUCKET_NAME` must exist before uploads work.
- `VITE_API_BASE_URL` must point to the backend API prefix, not just the server root.
- `JWT_SECRET` must be changed before any hosted deployment.
- `GSTN_API_BASE_URL` in this repository is still a placeholder; local testing works even if the external GSTN dependency is unavailable because the client degrades gracefully.

---

## 4. Local testing option A: run infra in Docker, app processes on your machine

Use this when you want faster code-edit/reload cycles for backend and frontend.

### Step 1: start PostgreSQL and Redis

```bash
docker-compose -f docker-compose.db.yml up -d
```

Wait until both containers are healthy enough to accept connections.

### Step 2: start MinIO separately

Because `docker-compose.db.yml` only starts PostgreSQL and Redis, start MinIO as a one-off local container:

```bash
docker run -d \
  --name compliance-minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio:latest server /data --console-address ":9001"
```

### Step 3: create the S3 bucket in MinIO

Open `http://localhost:9001`, sign in with:

- username: `minioadmin`
- password: `minioadmin`

Create a bucket named:

- `compliance-data`

Do this before trying any upload from the frontend or API.

### Step 4: create a Python virtual environment and install backend dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
```

### Step 5: run database migrations

```bash
cd backend
alembic upgrade head
cd ..
```

### Step 6: seed demo data

```bash
cd backend
PYTHONPATH=. python ../scripts/seed_demo_data.py
cd ..
```

This creates:

- tenant ID: `00000000-0000-0000-0000-000000000001`
- email: `ca@example.com`
- password: `password123`

### Step 7: run the FastAPI backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Keep this terminal open.

### Step 8: run the Celery worker in a second terminal

```bash
cd backend
source .venv/bin/activate
celery -A app.workers.tasks worker --loglevel=info
```

Keep this terminal open too.

### Step 9: install frontend dependencies and run Vite

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Then open:

- frontend: `http://localhost:5173`
- backend health check: `http://localhost:8000/health`
- MinIO console: `http://localhost:9001`

### Step 10: log in from the frontend

Use the seeded account:

- tenant ID: `00000000-0000-0000-0000-000000000001`
- email: `ca@example.com`
- password: `password123`

The frontend already defaults to the seeded tenant ID, so only the email and password normally need to be entered.

### Step 11: test the API manually before using the UI

#### Health check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

#### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'X-Tenant-Id: 00000000-0000-0000-0000-000000000001' \
  -d '{"email":"ca@example.com","password":"password123"}'
```

The response returns an `access_token`. Keep that token for any authenticated API testing.

### Step 12: test an upload end to end

1. Create or choose a CSV/XLS/XLSX invoice file.
2. Ensure the seeded client GSTIN exists: `27ABCDE1234F1Z5`.
3. Upload from the frontend **or** with curl.

Example API upload:

```bash
curl -X POST 'http://localhost:8000/api/v1/batches/upload?client_gstin=27ABCDE1234F1Z5' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'X-Tenant-Id: 00000000-0000-0000-0000-000000000001' \
  -F 'file=@/absolute/path/to/your-file.csv'
```

4. Copy the returned `batch_id`.
5. Poll progress:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'X-Tenant-Id: 00000000-0000-0000-0000-000000000001' \
  http://localhost:8000/api/v1/batches/YOUR_BATCH_ID/progress
```

6. Fetch results after processing completes:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'X-Tenant-Id: 00000000-0000-0000-0000-000000000001' \
  http://localhost:8000/api/v1/batches/YOUR_BATCH_ID/results
```

### Step 13: run backend unit tests

```bash
cd backend
source .venv/bin/activate
PYTHONPATH=. pytest tests/unit -v
```

### Step 14: stop local services when finished

Stop the app terminals with `Ctrl+C`, then clean up containers:

```bash
docker-compose -f docker-compose.db.yml down
docker rm -f compliance-minio
```

---

## 5. Local testing option B: run the full stack in Docker Compose

Use this when you want the most production-like local run with fewer manual terminals.

### Step 1: prepare the environment file

```bash
cp .env.example .env
```

### Step 2: verify the values used by Docker services

The Compose file overrides some network hostnames for containers internally:

- API container uses PostgreSQL at `postgres`
- API container uses Redis at `redis`
- API container uses MinIO at `minio`
- Worker uses the same internal service names
- Frontend still talks to `http://localhost:8000/api/v1`

You usually do not need to change `.env` for this mode beyond setting a real `JWT_SECRET`.

### Step 3: build and start the stack

```bash
docker-compose up --build
```

This starts:

- `postgres`
- `redis`
- `minio`
- `api`
- `worker`
- `frontend`

### Step 4: create the MinIO bucket

Even in full Compose mode, the storage bucket must exist before uploads can succeed.

Open `http://localhost:9001` and create:

- bucket: `compliance-data`

### Step 5: run database migrations inside the API container

Open a second terminal in the repo and run:

```bash
docker-compose exec api alembic upgrade head
```

### Step 6: seed demo data inside the API container

```bash
docker-compose exec api python /app/../scripts/seed_demo_data.py
```

If that path does not exist in the running container image because only `backend/` is copied into the image, use the host-run seed flow instead:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python ../scripts/seed_demo_data.py
cd ..
```

### Step 7: open the application

- frontend: `http://localhost:5173`
- backend health check: `http://localhost:8000/health`
- MinIO console: `http://localhost:9001`

### Step 8: sign in and test the workflow

Use the same seeded values:

- tenant ID: `00000000-0000-0000-0000-000000000001`
- email: `ca@example.com`
- password: `password123`

Then test:

1. Login
2. Upload a sample file for client GSTIN `27ABCDE1234F1Z5`
3. Watch batch progress
4. Open validation results
5. Open reconciliation results
6. Download an export

### Step 9: stop the stack

```bash
docker-compose down
```

Add `-v` if you want to remove persistent volumes too:

```bash
docker-compose down -v
```

---

## 6. What to verify during local testing

For a useful local verification pass, confirm all of the following:

### Backend verification checklist

- `GET /health` returns `200`
- login returns a bearer token
- `alembic upgrade head` completes without error
- upload creates a new batch row
- worker logs show the pipeline stages executing
- progress endpoint returns updated percentages/status
- results endpoint returns invoice, validation, and reconciliation data
- export endpoint returns a downloadable file

### Frontend verification checklist

- login page authenticates successfully
- dashboard loads without API errors
- batch upload form accepts a file and starts processing
- progress page updates over time
- validation and reconciliation pages render batch data
- export page triggers a download
- audit page loads data for the seeded tenant

---

## 7. Hosted deployment architecture

The repository is structured for this hosted layout:

- **Backend API** → Render Web Service
- **Worker** → Render Background Worker
- **PostgreSQL** → Render PostgreSQL
- **Redis** → Upstash Redis
- **Object storage** → Cloudflare R2 or AWS S3
- **Frontend** → Vercel

This separation matches the Phase 1 architecture more closely than trying to host everything on one service.

---

## 8. Hosted deployment: backend and worker

### Step 1: provision managed infrastructure first

Create these services before deploying application code:

1. **Render PostgreSQL database**
2. **Upstash Redis instance**
3. **Cloudflare R2 bucket** or **AWS S3 bucket**

Collect the following values:

- `DATABASE_URL`
- `REDIS_URL`
- `S3_ENDPOINT`
- `S3_ACCESS_KEY`
- `S3_SECRET_KEY`
- `S3_BUCKET_NAME`

Also choose and generate these secrets:

- `JWT_SECRET`
- `GSTN_API_KEY`
- `LLM_API_KEY` if used later

### Step 2: create the object bucket before first upload

Create the production bucket before the API accepts uploads.

Examples:

- R2 bucket name: `compliance-data-prod`
- S3 bucket name: `compliance-data-prod`

If you use R2, set `S3_ENDPOINT` to the account-specific R2 S3 endpoint.

### Step 3: create the Render web service for the API

Recommended settings:

- **Service type:** Web Service
- **Root directory:** `backend`
- **Runtime:** Python
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: add backend environment variables in Render

Set these on the API service:

```env
APP_ENV=production
DATABASE_URL=...
REDIS_URL=...
S3_ENDPOINT=...
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_BUCKET_NAME=...
JWT_SECRET=...
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GSTN_API_KEY=...
GSTN_API_BASE_URL=...
GSTN_CACHE_TTL=86400
LLM_API_KEY=
LOG_LEVEL=INFO
```

### Step 5: create the Render background worker for Celery

Recommended settings:

- **Service type:** Background Worker
- **Root directory:** `backend`
- **Runtime:** Python
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `celery -A app.workers.tasks worker --loglevel=info`

### Step 6: add the same environment variables to the worker

The worker must have the same values as the API for:

- database
- redis
- object storage
- JWT configuration
- GSTN settings
- logging settings

### Step 7: run migrations against the hosted database

Run Alembic once against the production database before using the app.

You can do this from a temporary shell or CI job with the production `DATABASE_URL`:

```bash
cd backend
export DATABASE_URL='YOUR_PRODUCTION_DATABASE_URL'
alembic upgrade head
```

### Step 8: seed an initial tenant and user

The repository contains a demo seed script. For production, either adapt that script or create your first tenant/user through a controlled bootstrap process.

If you intentionally want the demo seed values in a non-production test deployment:

```bash
cd backend
export DATABASE_URL='YOUR_PRODUCTION_DATABASE_URL'
PYTHONPATH=. python ../scripts/seed_demo_data.py
```

Do not use the demo password in a real production environment.

### Step 9: verify the hosted backend

Check the API directly:

```bash
curl https://YOUR_RENDER_API_URL/health
```

Then verify login:

```bash
curl -X POST https://YOUR_RENDER_API_URL/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'X-Tenant-Id: YOUR_TENANT_ID' \
  -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}'
```

### Step 10: confirm background processing works

After uploading a file through the frontend or API, confirm all of the following:

- API returns a `batch_id`
- worker logs show the batch being picked up
- progress endpoint changes over time
- results endpoint returns processed data
- exports download successfully

---

## 9. Hosted deployment: frontend on Vercel

### Step 1: create the Vercel project from `frontend/`

Use these project settings:

- **Framework preset:** Vite
- **Root directory:** `frontend`
- **Build command:** `npm run build`
- **Output directory:** `dist`

### Step 2: add the frontend environment variable

Set this in Vercel:

```env
VITE_API_BASE_URL=https://YOUR_RENDER_API_URL/api/v1
```

This must point to the deployed backend API prefix.

### Step 3: deploy the frontend

Once the build succeeds, open the Vercel URL and test:

1. Login
2. Dashboard load
3. Upload flow
4. Progress page
5. Validation results
6. Reconciliation results
7. Export actions

### Step 4: if browser CORS issues appear

The backend currently allows all origins in FastAPI CORS middleware, which is convenient for development. For a real production deployment, tighten CORS to your Vercel domain before going live.

---

## 10. Recommended hosted rollout order

Use this order so services do not fail due to missing dependencies:

1. Create PostgreSQL
2. Create Redis
3. Create object storage bucket
4. Set backend and worker environment variables
5. Deploy backend API
6. Deploy worker
7. Run migrations
8. Seed/bootstrap initial tenant and user
9. Deploy frontend with the final backend URL
10. Perform login, upload, progress, results, and export smoke tests

---

## 11. Common failure points and fixes

### Upload fails immediately

Check:

- the bucket exists
- `S3_ENDPOINT` is correct
- object storage credentials are valid
- `client_gstin` already exists in the database

### Login fails with 401

Check:

- `X-Tenant-Id` is correct
- the seeded or provisioned user exists in the same tenant
- password hash in the database matches the supplied password

### Batch never progresses

Check:

- worker is running
- worker can reach Redis
- worker can reach PostgreSQL
- worker can read the uploaded object from storage

### Frontend loads but API calls fail

Check:

- `VITE_API_BASE_URL` points to `/api/v1`
- backend URL is reachable from the browser
- token exists after login
- `X-Tenant-Id` is being sent

### Export fails

Check:

- the batch completed successfully
- the user role is `CA` or `ADMIN`
- the backend process has required Python dependencies installed

---

## 12. Minimal smoke test commands

Run these in order after deployment or local startup.

### Backend

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -H 'X-Tenant-Id: 00000000-0000-0000-0000-000000000001' \
  -d '{"email":"ca@example.com","password":"password123"}'
```

### Frontend

Open the browser to:

```text
http://localhost:5173
```

Then manually verify login, upload, progress, results, and export.
