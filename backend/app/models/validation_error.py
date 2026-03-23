from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Severity
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class ValidationErrorRecord(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "validation_errors"

    invoice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True)
    batch_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("upload_batches.id"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    severity: Mapped[Severity] = mapped_column(Enum(Severity, name="severity_enum"), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    actual_value: Mapped[str] = mapped_column(Text, nullable=False)
    expected_value: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    invoice = relationship("Invoice", back_populates="errors")
