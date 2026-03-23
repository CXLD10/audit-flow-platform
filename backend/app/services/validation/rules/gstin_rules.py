from app.models.enums import Severity
from app.services.validation.types import RuleError
from app.utils.gstin_utils import is_valid_gstin


def run(invoice):
    errors: list[RuleError] = []
    for field_name in ("supplier_gstin", "recipient_gstin"):
        value = getattr(invoice, field_name)
        if value and not is_valid_gstin(value):
            errors.append(
                RuleError(
                    rule_id="V010",
                    severity=Severity.CRITICAL,
                    invoice_id=invoice.id,
                    field_name=field_name,
                    actual_value=value,
                    expected_value="Valid GSTIN with checksum",
                    message=f"{field_name} is not a valid GSTIN",
                )
            )
    return errors
