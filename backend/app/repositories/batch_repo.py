from datetime import datetime, timezone
from uuid import UUID

from app.models.batch import UploadBatch
from app.models.enums import BatchStatus
from app.repositories.base import BaseRepository


class BatchRepository(BaseRepository[UploadBatch]):
    model = UploadBatch

    def create(self, **kwargs) -> UploadBatch:
        batch = UploadBatch(tenant_id=self.tenant_id, **kwargs)
        self.db.add(batch)
        return batch

    def list_paginated(self, *, page: int, page_size: int):
        return self._base_query().order_by(UploadBatch.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    def mark_processing(self, batch: UploadBatch) -> UploadBatch:
        batch.status = BatchStatus.PROCESSING
        return batch

    def mark_complete(self, batch: UploadBatch, *, total_invoices: int, error_count: int, last_completed_stage: str) -> UploadBatch:
        batch.status = BatchStatus.COMPLETE
        batch.total_invoices = total_invoices
        batch.error_count = error_count
        batch.last_completed_stage = last_completed_stage
        batch.completed_at = datetime.now(tz=timezone.utc)
        return batch

    def mark_failed(self, batch: UploadBatch, *, stage: str, error_message: str) -> UploadBatch:
        batch.status = BatchStatus.FAILED
        batch.failed_stage = stage
        batch.error_message = error_message
        return batch

    def update_checkpoint(self, batch: UploadBatch, *, stage: str, total_invoices: int | None = None, error_count: int | None = None) -> UploadBatch:
        batch.last_completed_stage = stage
        if total_invoices is not None:
            batch.total_invoices = total_invoices
        if error_count is not None:
            batch.error_count = error_count
        return batch
