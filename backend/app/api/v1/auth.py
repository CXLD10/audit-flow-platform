from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import CurrentUser, create_access_token, get_current_user
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, x_tenant_id: UUID = Header(..., alias="X-Tenant-Id"), db: Session = Depends(get_db)):
    token = AuthService(db=db, tenant_id=x_tenant_id).login(email=payload.email, password=payload.password)
    return TokenResponse(access_token=token)




@router.post("/refresh", response_model=TokenResponse)
def refresh(current_user: CurrentUser = Depends(get_current_user)):
    return TokenResponse(access_token=create_access_token(user_id=current_user.id, tenant_id=current_user.tenant_id, email=current_user.email, role=current_user.role))


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UserRepository(db=db, tenant_id=current_user.tenant_id).get_by_id(current_user.id)
    return user
