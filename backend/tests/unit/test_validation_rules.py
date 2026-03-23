from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from app.models.enums import Severity
from app.services.validation.rules import amount_rules, date_rules, duplicate_rules, gstin_rules
from app.services.validation.types import ValidationContext


def make_invoice(**overrides):
    values = {
        "id": uuid4(),
        "invoice_date": date(2025, 4, 1),
        "place_of_supply": "27",
        "supplier_gstin": "27ABCDE1234F1Z5",
        "recipient_gstin": "27ABCDE1234F1Z5",
        "taxable_value": Decimal("100.00"),
        "cgst_amount": Decimal("9.00"),
        "sgst_amount": Decimal("9.00"),
        "igst_amount": Decimal("0.00"),
        "total_invoice_value": Decimal("118.00"),
        "applicable_rate": Decimal("18.00"),
        "credit_note_flag": False,
        "invoice_number": "INV-001",
        "hsn_sac_code": "1001",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_gstin_rule_flags_invalid_gstin():
    invoice = make_invoice(supplier_gstin="INVALIDGSTIN000")
    errors = gstin_rules.run(invoice)
    assert errors[0].rule_id == "V010"


def test_date_rule_flags_future_date():
    invoice = make_invoice(invoice_date=date(2099, 1, 1))
    errors = date_rules.run(invoice)
    assert any(error.rule_id == "V012" for error in errors)


def test_amount_rule_flags_total_mismatch():
    invoice = make_invoice(total_invoice_value=Decimal("120.00"))
    errors = amount_rules.run(invoice)
    assert any(error.rule_id == "V022" for error in errors)


def test_duplicate_rule_flags_batch_duplicates():
    invoice = make_invoice()
    context = ValidationContext(invoice_count_by_key={(invoice.supplier_gstin, invoice.invoice_number): 2})
    errors = duplicate_rules.run(invoice, context)
    assert errors[0].severity == Severity.CRITICAL
