from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.invoice import InvoiceResponse
from app.schemas.validation_error import ValidationErrorResponse


class BatchUploadResponse(BaseModel):
    batch_id: UUID
    status: str


class BatchProgressResponse(BaseModel):
    stage: str
    pct: int
    processed: int
    total: int
    status: str
    error_message: str | None = None
    degraded: bool = False


class BatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    client_id: UUID
    user_id: UUID
    filename: str
    file_path_s3: str
    status: str
    return_period: date | None
    total_invoices: int
    error_count: int
    created_at: datetime
    completed_at: datetime | None
    failed_stage: str | None
    error_message: str | None
    last_completed_stage: str | None


class BatchResultsResponse(BaseModel):
    batch: BatchResponse
    invoices: list[InvoiceResponse]
    errors: list[ValidationErrorResponse]
    degraded_messages: list[str]
