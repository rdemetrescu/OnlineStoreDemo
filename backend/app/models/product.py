from typing import Optional

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    available: Optional[bool]
    price: Optional[float]


class ProductCreate(ProductBase):
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
    price: float
