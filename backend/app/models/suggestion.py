from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import SuggestionDecision
from app.models.mixins import TenantScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Suggestion(UUIDPrimaryKeyMixin, TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "suggestions"

    invoice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    error_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("validation_errors.id"), nullable=False)
    suggestion_type: Mapped[str] = mapped_column(String(50), nullable=False)
    suggested_value: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[int] = mapped_column(nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    suppressed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class SuggestionDecisionRecord(UUIDPrimaryKeyMixin, TenantScopedMixin, Base):
    __tablename__ = "suggestion_decisions"

    suggestion_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("suggestions.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    decision: Mapped[SuggestionDecision] = mapped_column(Enum(SuggestionDecision, name="suggestion_decision_enum"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
