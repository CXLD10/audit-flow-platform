from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_email(self, email: str) -> User | None:
        return self._base_query().filter(User.email == email).one_or_none()

    def list_paginated(self, *, page: int, page_size: int):
        return self._base_query().order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
