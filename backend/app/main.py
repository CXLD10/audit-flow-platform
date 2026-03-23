from fastapi import FastAPI
<<<<<<< HEAD
=======
from fastapi.middleware.cors import CORSMiddleware
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c

from app.api.v1 import admin, auth, batches, clients, invoices
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title="AI Tax Compliance System", version="1.0.0")
<<<<<<< HEAD
=======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
app.include_router(auth.router, prefix="/api/v1")
app.include_router(batches.router, prefix="/api/v1")
app.include_router(invoices.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
