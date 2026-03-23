from decimal import Decimal
from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Client(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "clients"

    gstin: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    column_mapping: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    e_invoice_threshold_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    annual_turnover: Mapped[Decimal | None] = mapped_column(Numeric(15, 2, asdecimal=True), nullable=True)

    tenant = relationship("Tenant", back_populates="clients")
