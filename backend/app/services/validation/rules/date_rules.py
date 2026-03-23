<<<<<<< HEAD
from datetime import UTC, datetime
=======
from datetime import datetime, timezone
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c

from app.models.enums import Severity
from app.services.validation.types import RuleError
from app.utils.date_utils import financial_year_for, is_future


def run(invoice):
    errors: list[RuleError] = []
    if invoice.invoice_date is None:
        errors.append(RuleError("V011", Severity.CRITICAL, invoice.id, "invoice_date", "", "valid calendar date", "Invoice date is invalid"))
        return errors
    if is_future(invoice.invoice_date):
        errors.append(RuleError("V012", Severity.HIGH, invoice.id, "invoice_date", str(invoice.invoice_date), "not in the future", "Invoice date cannot be in the future"))
<<<<<<< HEAD
    current_fy = financial_year_for(datetime.now(tz=UTC).date())
=======
    current_fy = financial_year_for(datetime.now(tz=timezone.utc).date())
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
    if financial_year_for(invoice.invoice_date) < current_fy - 2:
        errors.append(RuleError("V013", Severity.LOW, invoice.id, "invoice_date", str(invoice.invoice_date), "within current or previous two financial years", "Invoice date is older than the previous two financial years"))
    return errors
