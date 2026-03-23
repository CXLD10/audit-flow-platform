from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import BatchStatus
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class UploadBatch(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "upload_batches"

    client_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path_s3: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[BatchStatus] = mapped_column(Enum(BatchStatus, name="batch_status_enum"), nullable=False, default=BatchStatus.PENDING)
    return_period: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_invoices: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_stage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_completed_stage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    client = relationship("Client")
    user = relationship("User")
    invoices = relationship("Invoice", back_populates="batch")
