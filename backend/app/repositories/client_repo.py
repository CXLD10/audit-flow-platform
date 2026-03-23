from uuid import UUID

from app.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    model = Client

    def list_paginated(self, *, page: int, page_size: int):
        return self._base_query().order_by(Client.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    def get_by_gstin(self, gstin: str) -> Client | None:
        return self._base_query().filter(Client.gstin == gstin).one_or_none()

    def create(self, **kwargs) -> Client:
        client = Client(tenant_id=self.tenant_id, **kwargs)
        self.db.add(client)
        return client
