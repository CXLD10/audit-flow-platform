import json


class GSTR1Generator:
    def build_draft(self, *, invoices):
        payload = {
            "watermark": "DRAFT — Review before filing. Not submitted to GSTN.",
            "invoices": [
                {
                    "invoice_number": invoice.invoice_number,
                    "invoice_date": invoice.invoice_date.isoformat() if invoice.invoice_date else None,
                    "supplier_gstin": invoice.supplier_gstin,
                    "recipient_gstin": invoice.recipient_gstin,
                    "total_invoice_value": str(invoice.total_invoice_value),
                }
                for invoice in invoices
            ],
        }
        return json.dumps(payload, indent=2).encode()
