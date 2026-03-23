from sqlalchemy.orm import Session

from app.repositories.client_repo import ClientRepository


class ClientService:
    def __init__(self, db: Session, tenant_id):
        self.db = db
        self.repo = ClientRepository(db=db, tenant_id=tenant_id)

    def list_clients(self, *, page: int, page_size: int):
        return self.repo.list_paginated(page=page, page_size=page_size)

    def create_client(self, **kwargs):
        client = self.repo.create(**kwargs)
        self.db.commit()
        self.db.refresh(client)
        return client
