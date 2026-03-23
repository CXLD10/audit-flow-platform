from collections import Counter
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import InvoiceState
from app.models.validation_error import ValidationErrorRecord
from app.repositories.error_repo import ErrorRepository
from app.repositories.hsn_repo import HSNRepository
from app.repositories.invoice_repo import InvoiceRepository
from app.services.state_machine import transition_invoice
from app.services.validation.rules import amount_rules, date_rules, duplicate_rules, gstin_rules, hsn_rules, place_of_supply_rules, schema_rules
from app.services.validation.types import RuleError, ValidationContext


class ValidationEngine:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id
        self.error_repo = ErrorRepository(db=db, tenant_id=tenant_id)
        self.invoice_repo = InvoiceRepository(db=db, tenant_id=tenant_id)
        self.hsn_repo = HSNRepository(db=db)

    def _build_context(self, invoices: list) -> ValidationContext:
        batch_counts = Counter((invoice.supplier_gstin, invoice.invoice_number) for invoice in invoices)
        historic_keys = set()
        for invoice in invoices:
            previous = self.invoice_repo.list_for_duplicate_check(
                client_id=invoice.client_id,
                invoice_number=invoice.invoice_number,
                supplier_gstin=invoice.supplier_gstin,
                exclude_batch_id=invoice.batch_id,
            )
            if previous:
                historic_keys.add((invoice.supplier_gstin, invoice.invoice_number))
        hsn_tax_rates = {}
        for invoice in invoices:
            record = self.hsn_repo.get_by_code(invoice.hsn_sac_code)
            if record:
                hsn_tax_rates[record.code] = record.tax_rate
        return ValidationContext(invoice_count_by_key=batch_counts, historic_invoice_keys=historic_keys, hsn_tax_rates=hsn_tax_rates)

    def validate_batch(self, invoices: list) -> list[ValidationErrorRecord]:
        context = self._build_context(invoices)
        persisted_errors: list[ValidationErrorRecord] = []
        for invoice in invoices:
            rule_errors: list[RuleError] = []
            rule_errors.extend(schema_rules.run(invoice))
            rule_errors.extend(gstin_rules.run(invoice))
            rule_errors.extend(date_rules.run(invoice))
            rule_errors.extend(place_of_supply_rules.run(invoice))
            rule_errors.extend(amount_rules.run(invoice))
            rule_errors.extend(hsn_rules.run(invoice, context.hsn_tax_rates))
            rule_errors.extend(duplicate_rules.run(invoice, context))
            transition_invoice(invoice=invoice, new_state=InvoiceState.VALIDATED, actor="system", db=self.db)
            if rule_errors:
                for item in rule_errors:
                    persisted_errors.append(
                        ValidationErrorRecord(
                            tenant_id=self.tenant_id,
                            invoice_id=item.invoice_id,
                            batch_id=invoice.batch_id,
                            rule_id=item.rule_id,
                            severity=item.severity,
                            field_name=item.field_name,
                            actual_value=item.actual_value,
                            expected_value=item.expected_value,
                            message=item.message,
                        )
                    )
                transition_invoice(invoice=invoice, new_state=InvoiceState.ERROR_FOUND, actor="system", db=self.db)
        if persisted_errors:
            self.error_repo.create_many(persisted_errors)
        return persisted_errors
