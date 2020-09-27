from typing import Optional

from app.models.core import BaseModel


class AddressBase(BaseModel):
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]


class AddressCreateUpdate(AddressBase):
    street: str
    city: str
    state: str
    zip: str
    country: str
