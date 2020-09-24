from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    skip: int = Query(0, ge=0)
    limit: int = Query(
        100, gt=0, le=1000
    )  # limit must bet between 1 and 1,000 (default = 100)
