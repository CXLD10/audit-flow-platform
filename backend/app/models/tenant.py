from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Tenant(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    plan_tier: Mapped[str] = mapped_column(String(50), nullable=False, default="starter")

    users = relationship("User", back_populates="tenant")
    clients = relationship("Client", back_populates="tenant")
