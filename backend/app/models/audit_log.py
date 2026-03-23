from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class AuditLog(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "audit_log"

    user_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
