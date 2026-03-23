from uuid import UUID

from celery import Celery

from app.core.config import settings
from app.core.database import WorkerSessionLocal
from app.core.logging import configure_logging, get_logger
from app.models.enums import BatchStatus
from app.repositories.batch_repo import BatchRepository
from app.workers.pipeline import PipelineRunner

configure_logging()
log = get_logger(__name__)
app = Celery("compliance", broker=settings.redis_url, backend=settings.redis_url)
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]
app.conf.task_track_started = True
app.conf.task_default_queue = "default"
app.conf.task_routes = {"app.workers.tasks.process_batch": {"queue": "default"}}


class HardFailureError(Exception):
    pass


@app.task(bind=True, max_retries=3, default_retry_delay=30, retry_backoff=True)
def process_batch(self, batch_id: str, tenant_id: str):
    db = WorkerSessionLocal()
    try:
        repository = BatchRepository(db=db, tenant_id=UUID(tenant_id))
        batch = repository.get_by_id(UUID(batch_id))
        if batch is None:
            log.error("batch_not_found", batch_id=batch_id, tenant_id=tenant_id)
            return None
        if batch.status == BatchStatus.COMPLETE:
            log.info("batch_already_complete", batch_id=batch_id, tenant_id=tenant_id)
            return None
        try:
            PipelineRunner(db=db, tenant_id=UUID(tenant_id)).run(UUID(batch_id))
        except (ValueError, FileNotFoundError) as exc:
            raise HardFailureError(str(exc)) from exc
        except HardFailureError:
            raise
        except Exception as exc:  # noqa: BLE001
            if self.request.retries >= self.max_retries:
                raise
            raise self.retry(exc=exc)
    finally:
        db.close()
