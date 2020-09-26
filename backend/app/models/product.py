from typing import Optional

from pydantic import validator
from pydantic.errors import NumberNotGtError

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    available: Optional[bool]
    price: Optional[float]

    @validator("price")
    def price_must_not_be_negative(cls, v):
        if v is not None and v < 0:
            raise NumberNotGtError(limit_value=0)
        return v


class ProductCreateUpdate(ProductBase):
    name: str
    available: bool
    price: float


class ProductUpdate(ProductBase):
    pass


class Product(IDModelMixin, DateTimeModelMixin, ProductBase):
    pass


class ProductInDB(IDModelMixin, DateTimeModelMixin, ProductBase):
    name: str
    available: bool
    price: float  # = price_validation
