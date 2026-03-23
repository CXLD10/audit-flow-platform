from decimal import Decimal
from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class EntityMapping(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "entity_mappings"

    raw_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False)
    similarity_score: Mapped[Decimal] = mapped_column(Numeric(5, 2, asdecimal=True), nullable=False)
    source_batch_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("upload_batches.id"), nullable=False)
    user_overridden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
