from typing import List, Optional

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin
from pydantic.types import PositiveInt

from .address import AddressBase, AddressCreateUpdate


class OrderItemBase(BaseModel):
    product_id: Optional[PositiveInt]
    qty: Optional[PositiveInt]


class OrderItemCreateUpdate(BaseModel):
    product_id: PositiveInt
    qty: PositiveInt


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItem(IDModelMixin, DateTimeModelMixin, OrderItemBase):
    order_id: Optional[int]
    product_name: Optional[str]
    price: Optional[float]
    total: Optional[float]


class OrderItemInDB(IDModelMixin, DateTimeModelMixin, OrderItemBase):
    order_id: int
    product_id: int
    product_name: str
    price: float
    qty: int
    total: float
