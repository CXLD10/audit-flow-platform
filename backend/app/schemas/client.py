from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ClientCreateRequest(BaseModel):
    gstin: str = Field(min_length=15, max_length=15)
    legal_name: str
    column_mapping: dict[str, str] = Field(default_factory=dict)
    e_invoice_threshold_enabled: bool = False
    annual_turnover: Decimal | None = Field(default=None, decimal_places=2)


class ClientResponse(ORMModel):
    id: UUID
    tenant_id: UUID
    gstin: str
    legal_name: str
    column_mapping: dict
    e_invoice_threshold_enabled: bool
    annual_turnover: Decimal | None
    created_at: datetime
