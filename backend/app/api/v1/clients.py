from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import Pagination
from app.core.database import get_db
from app.core.security import CurrentUser, require_role
from app.schemas.client import ClientCreateRequest, ClientResponse
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientResponse])
def list_clients(pagination: Pagination, current_user: CurrentUser = Depends(require_role("CA", "ADMIN")), db: Session = Depends(get_db)):
    page, page_size = pagination
    return ClientService(db=db, tenant_id=current_user.tenant_id).list_clients(page=page, page_size=page_size)


@router.post("", response_model=ClientResponse)
def create_client(payload: ClientCreateRequest, current_user: CurrentUser = Depends(require_role("CA", "ADMIN")), db: Session = Depends(get_db)):
    return ClientService(db=db, tenant_id=current_user.tenant_id).create_client(**payload.model_dump())
