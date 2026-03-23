from app.models.enums import Severity
from app.services.validation.types import RuleError

MANDATORY_FIELDS = [
    "invoice_number",
    "invoice_date",
    "supplier_gstin",
    "recipient_gstin",
    "hsn_sac_code",
    "taxable_value",
    "cgst_amount",
    "sgst_amount",
    "igst_amount",
    "total_invoice_value",
    "place_of_supply",
]


def run(invoice):
    errors: list[RuleError] = []
    for field_name in MANDATORY_FIELDS:
        if getattr(invoice, field_name) in (None, ""):
            errors.append(
                RuleError(
                    rule_id="V001",
                    severity=Severity.CRITICAL,
                    invoice_id=invoice.id,
                    field_name=field_name,
                    actual_value="",
                    expected_value="non-empty value",
                    message=f"Mandatory field {field_name} is missing",
                )
            )
    return errors
