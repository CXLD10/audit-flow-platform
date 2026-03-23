from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import InvoiceState, MatchType
from app.models.reconciliation import ReconciliationResult
from app.repositories.reconciliation_repo import GSTR2BRepository, ReconciliationRepository
from app.services.reconciliation.blocking import filter_candidates
from app.services.reconciliation.matchers import exact_match, fuzzy_match, heuristic_match
from app.services.state_machine import transition_invoice


class ReconciliationEngine:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id
        self.gstr2b_repo = GSTR2BRepository(db=db, tenant_id=tenant_id)
        self.recon_repo = ReconciliationRepository(db=db, tenant_id=tenant_id)

    def reconcile(self, *, invoices: list, client_id: UUID, period: str) -> list[ReconciliationResult]:
        candidates = self.gstr2b_repo.list_by_client_period(client_id=client_id, period=period)
        results: list[ReconciliationResult] = []
        for invoice in invoices:
            blocked = filter_candidates(invoice, candidates)
            match = exact_match(invoice, blocked) or fuzzy_match(invoice, blocked) or heuristic_match(invoice, blocked)
            if match is None:
                match_type, confidence, candidate = MatchType.UNMATCHED, 0, None
                delta_taxable, delta_tax = invoice.taxable_value, invoice.cgst_amount + invoice.sgst_amount + invoice.igst_amount
            else:
                match_type, confidence, candidate = match
                delta_taxable = invoice.taxable_value - candidate.taxable_value
                delta_tax = (invoice.cgst_amount + invoice.sgst_amount + invoice.igst_amount) - candidate.tax_amount
            result = ReconciliationResult(
                tenant_id=self.tenant_id,
                invoice_id=invoice.id,
                gstr2b_record_id=candidate.id if candidate else None,
                match_type=match_type,
                confidence_score=confidence,
                delta_taxable_value=delta_taxable.quantize(Decimal("0.01")),
                delta_tax_amount=delta_tax.quantize(Decimal("0.01")),
            )
            self.recon_repo.upsert(result)
            transition_invoice(invoice=invoice, new_state=InvoiceState.RECONCILED, actor="system", db=self.db)
            results.append(result)
        return results
