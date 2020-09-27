from typing import List, Optional

from click.core import Option

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin
from pydantic.types import PositiveInt

from .address import AddressBase, AddressCreateUpdate

from .order_item import OrderItemCreateUpdate, OrderItemInDB, OrderItem


class OrderBase(BaseModel):
    billing_address: Optional[AddressBase]
    shipping_address: Optional[AddressBase]


class OrderCreateUpdate(OrderBase):
    billing_address: AddressCreateUpdate
    shipping_address: AddressCreateUpdate
    items: List[OrderItemCreateUpdate]


class OrderUpdate(OrderBase):
    pass


class Order(IDModelMixin, DateTimeModelMixin, OrderBase):
    billing_address: AddressBase
    shipping_address: AddressBase
    total: float


class OrderWithItems(Order):
    items: List[OrderItem]


class OrderInDB(IDModelMixin, DateTimeModelMixin, OrderBase):
    billing_address: AddressBase
    shipping_address: AddressBase
    total: float


class OrderWithItemsInDB(OrderInDB):
    items: List[OrderItemInDB]