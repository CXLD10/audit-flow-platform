from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class HSNMaster(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "hsn_master"

    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2, asdecimal=True), nullable=False)
    refreshed_at: Mapped[date] = mapped_column(Date, nullable=False)
