from decimal import Decimal

from app.models.enums import InvoiceState
from app.models.invoice import Invoice
from app.services.state_machine import transition_invoice
from app.utils.date_utils import parse_date
from app.utils.decimal_utils import to_decimal
from app.utils.gstin_utils import normalize_gstin


class InvoiceNormalizer:
    @staticmethod
    def normalize(invoice: Invoice, db) -> Invoice:
        invoice.supplier_gstin = normalize_gstin(invoice.supplier_gstin)
        invoice.recipient_gstin = normalize_gstin(invoice.recipient_gstin)
        invoice.invoice_date = parse_date(invoice.invoice_date) if invoice.invoice_date else None
        invoice.taxable_value = to_decimal(invoice.taxable_value)
        invoice.cgst_amount = to_decimal(invoice.cgst_amount)
        invoice.sgst_amount = to_decimal(invoice.sgst_amount)
        invoice.igst_amount = to_decimal(invoice.igst_amount)
        invoice.total_invoice_value = to_decimal(invoice.total_invoice_value)
        if invoice.applicable_rate is not None:
            invoice.applicable_rate = to_decimal(invoice.applicable_rate)
        invoice.hsn_sac_code = invoice.hsn_sac_code.strip()
        if invoice.hsn_sac_code.isdigit():
            invoice.hsn_sac_code = invoice.hsn_sac_code.lstrip("0") or "0"
        invoice.invoice_number = invoice.invoice_number.strip()
        invoice.place_of_supply = invoice.place_of_supply.strip().zfill(2)
        transition_invoice(invoice=invoice, new_state=InvoiceState.NORMALIZED, actor="system", db=db)
        return invoice
