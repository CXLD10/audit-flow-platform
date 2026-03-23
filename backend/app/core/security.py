from collections.abc import Callable
<<<<<<< HEAD
from datetime import UTC, datetime, timedelta
=======
from datetime import datetime, timezone, timedelta
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
from typing import Annotated, Any
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenPayload(BaseModel):
    sub: str
    exp: int
    tenant_id: UUID
    role: str
    email: EmailStr
    token_type: str = settings.access_token_subject


class CurrentUser(BaseModel):
    id: UUID
    tenant_id: UUID
    email: EmailStr
    role: str


DbSession = Annotated[Session, Depends(get_db)]
TokenStr = Annotated[str, Depends(oauth2_scheme)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(*, user_id: UUID, tenant_id: UUID, email: str, role: str) -> str:
<<<<<<< HEAD
    expires_at = datetime.now(tz=UTC) + timedelta(minutes=settings.jwt_expire_minutes)
=======
    expires_at = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "exp": expires_at,
        "tenant_id": str(tenant_id),
        "email": email,
        "role": role,
        "token_type": settings.access_token_subject,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token") from exc
    return TokenPayload.model_validate(payload)


def get_current_user(token: TokenStr, db: DbSession) -> CurrentUser:
    payload = decode_token(token)
    user = UserRepository(db=db, tenant_id=payload.tenant_id).get_by_id(UUID(payload.sub))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return CurrentUser(id=user.id, tenant_id=user.tenant_id, email=user.email, role=user.role.value)


def require_role(*roles: str) -> Callable[[CurrentUser], CurrentUser]:
    def dependency(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency
