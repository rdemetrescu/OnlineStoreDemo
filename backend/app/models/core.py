from datetime import datetime

from pydantic import BaseModel


class IDModelMixin(BaseModel):
    id: int


class DateTimeModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
