import json
from uuid import UUID

import redis

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class ProgressService:
    def __init__(self):
        self.client = redis.from_url(settings.redis_url, decode_responses=True)

    def set(self, batch_id: UUID | str, payload: dict) -> None:
        try:
            self.client.setex(f"batch_progress:{batch_id}", settings.progress_ttl_seconds, json.dumps(payload, default=str))
        except redis.RedisError as exc:
            log.error("progress_cache_write_failed", batch_id=str(batch_id), error=str(exc))

    def get(self, batch_id: UUID | str) -> dict | None:
        try:
            raw = self.client.get(f"batch_progress:{batch_id}")
        except redis.RedisError as exc:
            log.error("progress_cache_read_failed", batch_id=str(batch_id), error=str(exc))
            return None
        return json.loads(raw) if raw else None
