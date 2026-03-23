from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import Query, Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id

    def _base_query(self) -> Query:
        return self.db.query(self.model).filter(self.model.tenant_id == self.tenant_id)

    def get_by_id(self, entity_id: UUID) -> ModelT | None:
        return self._base_query().filter(self.model.id == entity_id).one_or_none()

    def add(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        return instance
