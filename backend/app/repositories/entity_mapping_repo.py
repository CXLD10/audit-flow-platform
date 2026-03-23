from app.models.entity_mapping import EntityMapping
from app.repositories.base import BaseRepository


class EntityMappingRepository(BaseRepository[EntityMapping]):
    model = EntityMapping

    def get_by_raw_name(self, raw_name: str) -> EntityMapping | None:
        return self._base_query().filter(EntityMapping.raw_name == raw_name).one_or_none()

    def create(self, **kwargs) -> EntityMapping:
        mapping = EntityMapping(tenant_id=self.tenant_id, **kwargs)
        self.db.add(mapping)
        return mapping
