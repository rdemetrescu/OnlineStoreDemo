from typing import Optional

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin
from pydantic import Field

price_validation = Field(..., ge=0)


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    available: Optional[bool]
    price: Optional[float] = price_validation


class ProductCreate(ProductBase):
    name: str
    available: bool
    price: float = price_validation


class ProductUpdate(ProductBase):
    pass


class Product(IDModelMixin, DateTimeModelMixin, ProductBase):
    pass


class ProductInDB(IDModelMixin, DateTimeModelMixin, ProductBase):
    name: str
    available: bool
    price: float = price_validation
