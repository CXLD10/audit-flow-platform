from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import Pagination
from app.core.database import get_db
from app.core.security import CurrentUser, require_role
from app.schemas.invoice import InvoiceListResponse, InvoiceResolveRequest, InvoiceResponse
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("", response_model=InvoiceListResponse)
def list_invoices(batch_id: UUID, pagination: Pagination, current_user: CurrentUser = Depends(require_role("CA", "CLIENT", "ADMIN")), db: Session = Depends(get_db)):
    page, page_size = pagination
    items, total = InvoiceService(db=db, tenant_id=current_user.tenant_id).list_invoices(batch_id=batch_id, page=page, page_size=page_size)
    return InvoiceListResponse(items=items, total=total)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: UUID, current_user: CurrentUser = Depends(require_role("CA", "CLIENT", "ADMIN")), db: Session = Depends(get_db)):
    return InvoiceService(db=db, tenant_id=current_user.tenant_id).get_invoice(invoice_id)


@router.patch("/{invoice_id}/resolve", response_model=InvoiceResponse)
def resolve_invoice(invoice_id: UUID, payload: InvoiceResolveRequest, current_user: CurrentUser = Depends(require_role("CA", "ADMIN")), db: Session = Depends(get_db)):
    del payload
    return InvoiceService(db=db, tenant_id=current_user.tenant_id).resolve_invoice(invoice_id=invoice_id, actor=current_user.id)
