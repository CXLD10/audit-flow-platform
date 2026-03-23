import json

import redis

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class GSTNCache:
    def __init__(self):
        self.client = redis.from_url(settings.redis_url, decode_responses=True)

    def get(self, key: str):
        try:
            value = self.client.get(key)
        except redis.RedisError as exc:
            log.error("gstn_cache_read_failed", key=key, error=str(exc))
            return None
        return json.loads(value) if value else None

    def set(self, key: str, value: dict, ttl: int):
        try:
            self.client.setex(key, ttl, json.dumps(value, default=str))
        except redis.RedisError as exc:
            log.error("gstn_cache_write_failed", key=key, error=str(exc))
