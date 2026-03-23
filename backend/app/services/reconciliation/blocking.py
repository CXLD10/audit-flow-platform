from decimal import Decimal


def filter_candidates(invoice, candidates):
    month = invoice.invoice_date.month if invoice.invoice_date else None
    filtered = [candidate for candidate in candidates if candidate.supplier_gstin == invoice.supplier_gstin]
    if month is not None:
        filtered = [
            candidate
            for candidate in filtered
            if candidate.invoice_date is not None and abs(candidate.invoice_date.month - month) <= 1
        ]
    lower = invoice.taxable_value * Decimal("0.98")
    upper = invoice.taxable_value * Decimal("1.02")
    return [candidate for candidate in filtered if lower <= candidate.taxable_value <= upper]
