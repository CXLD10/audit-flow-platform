from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from app.models.enums import Severity


@dataclass(slots=True)
class RuleError:
    rule_id: str
    severity: Severity
    invoice_id: UUID
    field_name: str
    actual_value: str
    expected_value: str
    message: str


@dataclass(slots=True)
class ValidationContext:
    invoice_count_by_key: dict[tuple[str, str], int] = field(default_factory=dict)
    historic_invoice_keys: set[tuple[str, str]] = field(default_factory=set)
    hsn_tax_rates: dict[str, Decimal] = field(default_factory=dict)
