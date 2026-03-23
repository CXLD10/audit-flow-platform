from app.models.enums import Severity
from app.services.validation.types import RuleError, ValidationContext


def run(invoice, context: ValidationContext):
    errors: list[RuleError] = []
    key = (invoice.supplier_gstin, invoice.invoice_number)
    if context.invoice_count_by_key.get(key, 0) > 1:
        errors.append(RuleError("V030", Severity.CRITICAL, invoice.id, "invoice_number", invoice.invoice_number, "unique invoice number within supplier GSTIN for the batch", "Duplicate invoice number found within the same batch"))
    if key in context.historic_invoice_keys:
        errors.append(RuleError("V031", Severity.HIGH, invoice.id, "invoice_number", invoice.invoice_number, "not previously uploaded for the client", "Invoice number already exists in a previous batch for this client"))
    return errors
