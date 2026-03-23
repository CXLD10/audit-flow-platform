from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import admin, auth, batches, clients, invoices
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title="AI Tax Compliance System", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(batches.router, prefix="/api/v1")
app.include_router(invoices.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
