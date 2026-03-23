from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ValidationErrorSchema(BaseModel):
    rule_id: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    invoice_id: UUID
    field_name: str
    actual_value: str
    expected_value: str
    message: str


class ValidationErrorResponse(ORMModel, ValidationErrorSchema):
    id: UUID
