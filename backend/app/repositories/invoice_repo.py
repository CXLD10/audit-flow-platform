from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import and_

from app.models.enums import InvoiceState
from app.models.invoice import Invoice
from app.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    model = Invoice

    def list_by_batch(self, batch_id: UUID, *, page: int = 1, page_size: int = 100):
        return (
            self._base_query()
            .filter(Invoice.batch_id == batch_id)
            .order_by(Invoice.created_at.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    def list_all_by_batch(self, batch_id: UUID):
        return self._base_query().filter(Invoice.batch_id == batch_id).order_by(Invoice.created_at.asc()).all()

    def create_many(self, invoices: Iterable[Invoice]) -> None:
        self.db.add_all(list(invoices))

    def get_existing_unique(self, *, client_id: UUID, batch_id: UUID, invoice_number: str, supplier_gstin: str) -> Invoice | None:
        return (
            self._base_query()
            .filter(
                Invoice.client_id == client_id,
                Invoice.batch_id == batch_id,
                Invoice.invoice_number == invoice_number,
                Invoice.supplier_gstin == supplier_gstin,
            )
            .one_or_none()
        )

    def list_for_duplicate_check(self, *, client_id: UUID, invoice_number: str, supplier_gstin: str, exclude_batch_id: UUID | None = None):
        query = self._base_query().filter(
            Invoice.client_id == client_id,
            Invoice.invoice_number == invoice_number,
            Invoice.supplier_gstin == supplier_gstin,
        )
        if exclude_batch_id is not None:
            query = query.filter(Invoice.batch_id != exclude_batch_id)
        return query.all()

    def list_by_state(self, *, batch_id: UUID, state: InvoiceState):
        return self._base_query().filter(and_(Invoice.batch_id == batch_id, Invoice.state == state)).all()
