from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import Pagination
from app.core.database import get_db
from app.core.security import CurrentUser, require_role
from app.schemas.auth import UserResponse
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/audit-logs")
def list_audit_logs(pagination: Pagination, current_user: CurrentUser = Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    page, page_size = pagination
    return AdminService(db=db, tenant_id=current_user.tenant_id).list_audit_logs(page=page, page_size=page_size)


@router.get("/users", response_model=list[UserResponse])
def list_users(pagination: Pagination, current_user: CurrentUser = Depends(require_role("ADMIN")), db: Session = Depends(get_db)):
    page, page_size = pagination
    return AdminService(db=db, tenant_id=current_user.tenant_id).list_users(page=page, page_size=page_size)
