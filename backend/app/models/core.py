from datetime import datetime

from pydantic import BaseModel, PositiveInt


class IDModelMixin(BaseModel):
    id: PositiveInt


class DateTimeModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
