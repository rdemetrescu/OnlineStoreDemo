from datetime import datetime

from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id: int = Field(..., gt=0)


class DateTimeModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
