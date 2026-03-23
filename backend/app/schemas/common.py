from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import settings


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=settings.default_page_size, ge=1, le=settings.max_page_size)


class MessageResponse(BaseModel):
    message: str
    detail: str | None = None
    id: UUID | None = None
