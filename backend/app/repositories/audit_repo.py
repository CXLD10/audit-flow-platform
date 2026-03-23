from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    model = AuditLog

    def write(self, **kwargs) -> AuditLog:
        record = AuditLog(tenant_id=self.tenant_id, **kwargs)
        self.db.add(record)
        return record

    def list_paginated(self, *, page: int, page_size: int):
        return self._base_query().order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
