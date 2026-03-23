import asyncio
from dataclasses import dataclass, field

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.services.gstn.cache import GSTNCache

log = get_logger(__name__)


@dataclass
class DegradedResult:
    success: bool = False
    data: dict = field(default_factory=dict)
    error_reason: str = ""
    degraded: bool = True


class GSTNApiClient:
    def __init__(self):
        self.cache = GSTNCache()

    async def verify_gstin(self, gstin: str):
        cache_key = f"gstin_status:{gstin}"
        cached = self.cache.get(cache_key)
        if cached:
            return DegradedResult(success=True, data={**cached, "cached": True}, degraded=False)
        try:
            async with httpx.AsyncClient(timeout=settings.gstn_timeout_seconds) as client:
                response = await client.get(
                    f"{settings.gstn_api_base_url.rstrip('/')}/taxpayer/{gstin}",
                    headers={"x-api-key": settings.gstn_api_key},
                )
                response.raise_for_status()
                data = response.json()
                self.cache.set(cache_key, data, settings.gstn_cache_ttl)
                return DegradedResult(success=True, data={**data, "cached": False}, degraded=False)
        except Exception as exc:  # noqa: BLE001
            log.error("gstn_call_failed", gstin=gstin, error=str(exc))
            return DegradedResult(error_reason=str(exc))

    async def verify_many(self, gstins: list[str]) -> dict[str, DegradedResult]:
        semaphore = asyncio.Semaphore(settings.gstn_max_concurrency)

        async def bounded(gstin: str):
            async with semaphore:
                return gstin, await self.verify_gstin(gstin)

        results = await asyncio.gather(*(bounded(gstin) for gstin in gstins))
        return dict(results)
