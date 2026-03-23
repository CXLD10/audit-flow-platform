from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.audit_repo import AuditRepository


def write_audit_log(*, db: Session, tenant_id: UUID, user_id: UUID | None, action_type: str, entity_type: str, entity_id: UUID, metadata: dict) -> None:
    AuditRepository(db=db, tenant_id=tenant_id).write(
        user_id=user_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata,
    )
