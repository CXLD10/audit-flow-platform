# AI Tax Compliance System

A production-oriented GST compliance validation and reconciliation platform for CA firms and SMEs in India. This monorepo implements the full Phase 1 architecture from the provided contexts:

- **Backend:** FastAPI + Celery + PostgreSQL + Redis.
- **Frontend:** React 18 + React Query + React Router.
- **Storage:** S3-compatible object storage (MinIO locally, R2/S3 in production).
- **Infra:** Docker Compose for local and pre-deployment verification.
- **Data model:** tenant-scoped PostgreSQL schema with auditability and Decimal-safe monetary fields.

---

## 1. Product Scope

The platform processes GST invoice uploads through a deterministic pipeline:

`Upload → Parse → Normalize → Entity Resolution → Validation → GSTN Verification → Reconciliation → Prioritization → Review → Export`

Key production rules implemented in the codebase:

- `Decimal` for all monetary values.
- Tenant isolation at the repository layer.
- RBAC at the API layer.
- Sync SQLAlchemy only.
- Idempotent Celery processing using `batch_id`.
- Audit logging for invoice state transitions.
- Graceful degradation for GSTN dependency failures.

---

## 2. Monorepo Layout

```text
backend/   FastAPI app, Celery worker, Alembic migrations, tests
frontend/  React/Vite application
infra/     infrastructure artifacts
scripts/   operational helpers and seed scripts
docs/      architecture and supporting documentation
```

See `docs/architecture.md` for the high-level flow and service map.

---

## 3. Backend Architecture

### Core modules
- `app/core/config.py` – validated environment configuration.
- `app/core/database.py` – sync SQLAlchemy engine/session factories for API and worker.
- `app/core/security.py` – JWT token handling and `require_role()` RBAC dependency.
- `app/core/logging.py` – `structlog` JSON logging.

### Data model
The schema includes the operational tables defined in the contexts plus implementation support fields required for execution:

- `tenants`
- `users`
- `clients`
- `upload_batches`
- `invoices`
- `validation_errors`
- `gstr2b_records`
- `reconciliation_results`
- `entity_mappings`
- `suggestions`
- `suggestion_decisions`
- `audit_log`
- `hsn_master`

All business tables include `tenant_id` to align with the approved conflict resolution and repository-enforced isolation model.

### Repository and service boundaries
- Routes do not contain business logic.
- Services orchestrate domain operations.
- Repository classes own all tenant-scoped query access.
- S3 access is isolated to `app/services/storage/s3_client.py`.
- GSTN HTTP access is isolated to `app/services/gstn/client.py`.

---

## 4. Processing Pipeline

### Upload flow
1. `POST /api/v1/batches/upload`
2. File validation at API layer (`csv`, `xlsx`, `xls`, max 50MB)
3. Raw file persisted to object storage under the tenant-prefixed path
4. `upload_batches` row created in PostgreSQL
5. Celery task enqueued immediately
6. Frontend polls progress from Redis every 2 seconds

### Worker stages
The worker executes the following stages sequentially:

1. **Parsing** – chunked CSV or streamed Excel ingestion, header detection, column mapping, invoice creation.
2. **Normalization** – GSTIN/date/amount/HSN/place-of-supply normalization.
3. **Entity resolution** – vendor canonicalization using RapidFuzz.
4. **Validation** – deterministic rule evaluation and fixed-schema error persistence.
5. **GSTN verification** – cached/degraded external verification.
6. **Reconciliation** – blocking + matching against GSTR-2B data.
7. **Prioritization** – severity-first ordering for review and reporting.

### State machine
Invoices follow the approved transition map:

- `RAW → PARSED`
- `PARSED → NORMALIZED`
- `NORMALIZED → VALIDATED`
- `VALIDATED → ERROR_FOUND`
- `VALIDATED → RECONCILED`
- `ERROR_FOUND → RECONCILED`
- `RECONCILED → REVIEWED`
- `REVIEWED → RESOLVED`
- `RESOLVED → EXPORTED`

`NORMALIZED → ERROR_FOUND` is intentionally not allowed.

---

## 5. Frontend Application

The frontend is intentionally functional and operational rather than design-heavy.

### Pages
- `Login`
- `Dashboard`
- `BatchUpload`
- `BatchProgress`
- `ValidationResults`
- `ReconciliationResults`
- `ClientManagement`
- `AuditLog`
- `ExportPage`

### Frontend patterns
- Axios API client with tenant + JWT headers.
- React Query for polling and server-state caching.
- Zustand auth store.
- `RoleGuard` for role-aware UI visibility.

---

## 6. Local Development

### Mode 1 – database + Redis only
```bash
docker-compose -f docker-compose.db.yml up -d
cp .env.example .env
cd backend && pip install -r requirements.txt
cd backend && alembic upgrade head
cd backend && uvicorn app.main:app --reload --port 8000
cd backend && celery -A app.workers.tasks worker --loglevel=info
cd frontend && npm install && npm run dev
```

### Mode 2 – production-like Compose
```bash
docker-compose up --build
```

---

## 7. Environment Variables

Copy `.env.example` to `.env` and provide values for:

- `DATABASE_URL`
- `REDIS_URL`
- `S3_ENDPOINT`
- `S3_ACCESS_KEY`
- `S3_SECRET_KEY`
- `S3_BUCKET_NAME`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`
- `GSTN_API_KEY`
- `GSTN_API_BASE_URL`
- `GSTN_CACHE_TTL`
- `LLM_API_KEY`
- `APP_ENV`
- `LOG_LEVEL`
- `VITE_API_BASE_URL`

---

## 8. Migrations and Seed Data

### Apply schema
```bash
cd backend
alembic upgrade head
```

### Seed demo tenant/user/client
```bash
cd backend
PYTHONPATH=. python ../scripts/seed_demo_data.py
```

Demo login values created by the seed script:

- Tenant ID: `00000000-0000-0000-0000-000000000001`
- Email: `ca@example.com`
- Password: `password123`

---

## 9. Testing

### Python unit tests
```bash
cd backend
PYTHONPATH=. pytest tests/unit -v
```

Current unit coverage includes:
- Decimal utilities
- Invoice state transition rules
- Repository tenant isolation
- Core validation rule behavior

---

## 10. Deployment Strategy

The repository includes a free-tier compatible deployment path matching the contexts:

- **Backend API:** Render Web Service
- **Celery worker:** Render Background Worker
- **Frontend:** Vercel
- **PostgreSQL:** Render PostgreSQL
- **Redis:** Upstash
- **Object storage:** Cloudflare R2

The included Dockerfiles and Compose manifests are intended for local validation before deploying to those managed services.

---

## 11. Known Next Steps

The current implementation now covers the requested repository structure, backend, worker, API, frontend, infra, migrations, and critical tests. The next iteration would typically deepen:

- richer GSTN and GSTR-2B integrations
- production auth/bootstrap flows
- broader validation/reconciliation test coverage
- export styling refinement
- Phase 2 suggestion engine activation
