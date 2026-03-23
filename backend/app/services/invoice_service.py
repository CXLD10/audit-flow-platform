from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import InvoiceState
from app.repositories.invoice_repo import InvoiceRepository
from app.services.state_machine import transition_invoice


class InvoiceService:
    def __init__(self, db: Session, tenant_id):
        self.db = db
        self.repo = InvoiceRepository(db=db, tenant_id=tenant_id)

    def list_invoices(self, *, batch_id, page: int, page_size: int):
        items = self.repo.list_by_batch(batch_id, page=page, page_size=page_size)
        total = len(self.repo.list_all_by_batch(batch_id))
        return items, total

    def get_invoice(self, invoice_id):
        invoice = self.repo.get_by_id(invoice_id)
        if invoice is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
        return invoice

    def resolve_invoice(self, *, invoice_id, actor):
        invoice = self.get_invoice(invoice_id)
        if invoice.state != InvoiceState.REVIEWED:
            if invoice.state == InvoiceState.RECONCILED:
                transition_invoice(invoice=invoice, new_state=InvoiceState.REVIEWED, actor=actor, db=self.db)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invoice must be reconciled before resolution")
        transition_invoice(invoice=invoice, new_state=InvoiceState.RESOLVED, actor=actor, db=self.db)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
