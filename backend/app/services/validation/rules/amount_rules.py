from decimal import Decimal

from app.models.enums import Severity
from app.services.validation.types import RuleError
from app.utils.decimal_utils import ONE_RUPEE, ZERO, within_tolerance


def run(invoice):
    errors: list[RuleError] = []
    intra_state = invoice.place_of_supply == invoice.supplier_gstin[:2]
    if intra_state and invoice.igst_amount > ZERO:
        errors.append(RuleError("V020", Severity.CRITICAL, invoice.id, "igst_amount", str(invoice.igst_amount), "IGST should be zero for intra-state supplies", "IGST cannot be present for intra-state supply"))
    if not intra_state and (invoice.cgst_amount > ZERO or invoice.sgst_amount > ZERO) and invoice.igst_amount > ZERO:
        errors.append(RuleError("V020", Severity.CRITICAL, invoice.id, "igst_amount", str(invoice.igst_amount), "Use only IGST for inter-state supplies", "CGST/SGST and IGST cannot both be present"))
    if invoice.taxable_value <= ZERO and not invoice.credit_note_flag:
        errors.append(RuleError("V024", Severity.HIGH, invoice.id, "taxable_value", str(invoice.taxable_value), "positive non-zero value", "Taxable value must be positive and non-zero"))
    if invoice.taxable_value < ZERO and not invoice.credit_note_flag:
        errors.append(RuleError("V025", Severity.HIGH, invoice.id, "taxable_value", str(invoice.taxable_value), "negative values allowed only for credit notes", "Negative taxable values require the credit note flag"))
    if invoice.applicable_rate is not None:
        expected_tax = (invoice.taxable_value * invoice.applicable_rate / Decimal("100.00")).quantize(Decimal("0.01"))
        actual_tax = invoice.cgst_amount + invoice.sgst_amount + invoice.igst_amount
        if not within_tolerance(actual_tax, expected_tax, ONE_RUPEE):
            errors.append(RuleError("V021", Severity.HIGH, invoice.id, "applicable_rate", str(actual_tax), str(expected_tax), "Tax amount does not match taxable value × applicable rate within tolerance"))
    expected_total = invoice.taxable_value + invoice.cgst_amount + invoice.sgst_amount + invoice.igst_amount
    if not within_tolerance(invoice.total_invoice_value, expected_total, ONE_RUPEE):
        errors.append(RuleError("V022", Severity.HIGH, invoice.id, "total_invoice_value", str(invoice.total_invoice_value), str(expected_total), "Total invoice value does not equal taxable + tax amounts within tolerance"))
    return errors
