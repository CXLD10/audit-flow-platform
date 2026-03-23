import uuid
<<<<<<< HEAD
from datetime import UTC, datetime
=======
from datetime import datetime, timezone
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
<<<<<<< HEAD
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=UTC), nullable=False)
=======
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), nullable=False)
>>>>>>> 1a35cbb7ff30d77ac34b907e8d1807c54670719c


class TenantScopedMixin:
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)


MetadataJSON = JSONB
