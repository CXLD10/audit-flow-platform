# Architecture Overview

## Monorepo
- `backend/`: FastAPI, Celery, SQLAlchemy, Alembic, services, repositories, tests.
- `frontend/`: React + Vite + React Query UI for upload, progress, validation, reconciliation, audit, and export.
- `infra/`: deployment and environment artifacts.
- `scripts/`: operational helpers such as demo seed data.

## Backend execution model
1. API authenticates the caller and uploads the raw batch to object storage.
2. Celery receives a `process_batch` task keyed by `batch_id`.
3. The worker runs parsing, normalization, entity resolution, validation, GSTN verification, reconciliation, and prioritization sequentially.
4. Redis stores progress and external cache entries.
5. PostgreSQL stores operational state, invoices, errors, reconciliation results, and audit logs.

## Reliability decisions
- All monetary values use `Decimal` and `Numeric(..., asdecimal=True)`.
- Tenant isolation is enforced in `BaseRepository`.
- Invoice state transitions are audited through `transition_invoice()`.
- GSTN failures degrade gracefully instead of crashing the worker.
