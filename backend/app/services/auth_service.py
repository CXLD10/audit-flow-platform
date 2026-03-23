from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, db: Session, tenant_id):
        self.user_repo = UserRepository(db=db, tenant_id=tenant_id)

    def login(self, *, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return create_access_token(user_id=user.id, tenant_id=user.tenant_id, email=user.email, role=user.role.value)
