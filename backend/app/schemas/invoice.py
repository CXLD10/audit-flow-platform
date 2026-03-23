from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.reconciliation import ReconciliationResultResponse
from app.schemas.validation_error import ValidationErrorResponse


class InvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: date | None = None
    supplier_name: str | None = None
    supplier_gstin: str
    recipient_gstin: str
    hsn_sac_code: str
    taxable_value: Decimal = Field(decimal_places=2)
    cgst_amount: Decimal = Field(decimal_places=2)
    sgst_amount: Decimal = Field(decimal_places=2)
    igst_amount: Decimal = Field(decimal_places=2)
    total_invoice_value: Decimal = Field(decimal_places=2)
    place_of_supply: str
    applicable_rate: Decimal | None = Field(default=None, decimal_places=2)
    credit_note_flag: bool = False


class InvoiceResponse(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    batch_id: UUID
    client_id: UUID
    canonical_supplier_name: str | None = None
    state: str
    gstn_verification_status: str | None = None
    created_at: datetime
    errors: list[ValidationErrorResponse] = Field(default_factory=list)
    reconciliation_result: ReconciliationResultResponse | None = None


class InvoiceResolveRequest(BaseModel):
    acknowledge: bool = True


class InvoiceListResponse(BaseModel):
    items: list[InvoiceResponse]
    total: int
