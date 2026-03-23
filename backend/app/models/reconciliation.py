from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MatchType
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class GSTR2BRecord(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "gstr2b_records"

    client_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    gstin: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    invoice_number: Mapped[str] = mapped_column(String(255), nullable=False)
    invoice_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    supplier_gstin: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    taxable_value: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)
    period: Mapped[str] = mapped_column(String(7), nullable=False, index=True)
    source_file: Mapped[str] = mapped_column(String(255), nullable=False)


class ReconciliationResult(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "reconciliation_results"

    invoice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False, index=True, unique=True)
    gstr2b_record_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("gstr2b_records.id"), nullable=True)
    match_type: Mapped[MatchType] = mapped_column(Enum(MatchType, name="match_type_enum"), nullable=False)
    confidence_score: Mapped[int] = mapped_column(nullable=False)
    delta_taxable_value: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)
    delta_tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)

    invoice = relationship("Invoice", back_populates="reconciliation_result")
