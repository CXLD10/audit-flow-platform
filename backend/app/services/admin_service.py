from sqlalchemy.orm import Session

from app.repositories.audit_repo import AuditRepository
from app.repositories.user_repo import UserRepository


class AdminService:
    def __init__(self, db: Session, tenant_id):
        self.audit_repo = AuditRepository(db=db, tenant_id=tenant_id)
        self.user_repo = UserRepository(db=db, tenant_id=tenant_id)

    def list_audit_logs(self, *, page: int, page_size: int):
        records = self.audit_repo.list_paginated(page=page, page_size=page_size)
        return [
            {
                "id": record.id,
                "action_type": record.action_type,
                "entity_type": record.entity_type,
                "entity_id": record.entity_id,
                "created_at": record.created_at,
                "metadata": record.metadata_,
            }
            for record in records
        ]

    def list_users(self, *, page: int, page_size: int):
        return self.user_repo.list_paginated(page=page, page_size=page_size)
