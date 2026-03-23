from typing import Annotated

from fastapi import Depends, Query

from app.core.config import settings


def pagination_params(page: int = Query(1, ge=1), page_size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size)) -> tuple[int, int]:
    return page, page_size


Pagination = Annotated[tuple[int, int], Depends(pagination_params)]
