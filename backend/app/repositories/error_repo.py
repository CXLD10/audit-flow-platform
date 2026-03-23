from uuid import UUID

from app.models.validation_error import ValidationErrorRecord
from app.repositories.base import BaseRepository


class ErrorRepository(BaseRepository[ValidationErrorRecord]):
    model = ValidationErrorRecord

    def create_many(self, errors: list[ValidationErrorRecord]) -> None:
        self.db.add_all(errors)

    def list_by_batch(self, batch_id: UUID):
        return self._base_query().filter(ValidationErrorRecord.batch_id == batch_id).order_by(ValidationErrorRecord.created_at.asc()).all()

    def count_by_batch(self, batch_id: UUID) -> int:
        return self._base_query().filter(ValidationErrorRecord.batch_id == batch_id).count()
