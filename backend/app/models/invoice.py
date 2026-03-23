from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Index, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import GSTNVerificationStatus, InvoiceState
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Invoice(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "invoices"
    __table_args__ = (
        Index("ix_invoices_tenant_batch", "tenant_id", "batch_id"),
        Index("ix_invoices_tenant_state", "tenant_id", "state"),
    )

    batch_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("upload_batches.id"), nullable=False, index=True)
    client_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    invoice_number: Mapped[str] = mapped_column(String(255), nullable=False)
    invoice_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    supplier_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    canonical_supplier_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    supplier_gstin: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    recipient_gstin: Mapped[str] = mapped_column(String(15), nullable=False)
    hsn_sac_code: Mapped[str] = mapped_column(String(20), nullable=False)
    taxable_value: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)
    cgst_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False, default=Decimal("0.00"))
    sgst_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False, default=Decimal("0.00"))
    igst_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False, default=Decimal("0.00"))
    total_invoice_value: Mapped[Decimal] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=False)
    place_of_supply: Mapped[str] = mapped_column(String(2), nullable=False)
    applicable_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2, asdecimal=True), nullable=True)
    state: Mapped[InvoiceState] = mapped_column(Enum(InvoiceState, name="invoice_state_enum"), nullable=False, default=InvoiceState.RAW)
    gstn_verification_status: Mapped[GSTNVerificationStatus | None] = mapped_column(
        Enum(GSTNVerificationStatus, name="gstn_verification_status_enum"), nullable=True
    )
    credit_note_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_row_number: Mapped[int | None] = mapped_column(nullable=True)

    batch = relationship("UploadBatch", back_populates="invoices")
    errors = relationship("ValidationErrorRecord", back_populates="invoice")
    reconciliation_result = relationship("ReconciliationResult", back_populates="invoice", uselist=False)
