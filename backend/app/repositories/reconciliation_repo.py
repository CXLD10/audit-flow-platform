from uuid import UUID

from app.models.reconciliation import GSTR2BRecord, ReconciliationResult
from app.repositories.base import BaseRepository


class ReconciliationRepository(BaseRepository[ReconciliationResult]):
    model = ReconciliationResult

    def upsert(self, result: ReconciliationResult) -> ReconciliationResult:
        existing = self._base_query().filter(ReconciliationResult.invoice_id == result.invoice_id).one_or_none()
        if existing is None:
            self.db.add(result)
            return result
        existing.gstr2b_record_id = result.gstr2b_record_id
        existing.match_type = result.match_type
        existing.confidence_score = result.confidence_score
        existing.delta_taxable_value = result.delta_taxable_value
        existing.delta_tax_amount = result.delta_tax_amount
        return existing


class GSTR2BRepository(BaseRepository[GSTR2BRecord]):
    model = GSTR2BRecord

    def list_by_client_period(self, *, client_id: UUID, period: str):
        return self._base_query().filter(GSTR2BRecord.client_id == client_id, GSTR2BRecord.period == period).all()
