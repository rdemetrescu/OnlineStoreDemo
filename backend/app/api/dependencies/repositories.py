from typing import Callable, Type

from databases import Database
from fastapi import Depends

from app.api.dependencies.database import get_database
from app.db.repositories.base import BaseRepository


def get_repository(repository_type: Type[BaseRepository]) -> Callable:
    def __get_repository(db: Database = Depends(get_database)) -> BaseRepository:
        return repository_type(db)

    return __get_repository
