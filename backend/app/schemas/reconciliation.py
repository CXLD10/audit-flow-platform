from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ReconciliationResultResponse(ORMModel):
    id: UUID
    invoice_id: UUID
    gstr2b_record_id: UUID | None
    match_type: str
    confidence_score: int = Field(ge=0, le=100)
    delta_taxable_value: Decimal
    delta_tax_amount: Decimal
    created_at: datetime
