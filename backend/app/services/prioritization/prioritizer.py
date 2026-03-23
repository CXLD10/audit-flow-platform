from datetime import date

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


class ErrorPrioritizer:
    @staticmethod
    def sort_errors(errors, invoices_by_id):
        return sorted(
            errors,
            key=lambda error: (
                SEVERITY_ORDER.get(error.severity.value if hasattr(error.severity, "value") else error.severity, 99),
                invoices_by_id[error.invoice_id].invoice_date or date.min,
            ),
        )
