from typing import Optional

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin
from pydantic import EmailStr


class CustomerBase(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]


class CustomerCreate(CustomerBase):
    name: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    zip: str
    country: str


class CustomerUpdate(CustomerBase):
    name: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    zip: str
    country: str


class Customer(IDModelMixin, DateTimeModelMixin, CustomerBase):
    pass


class CustomerInDB(IDModelMixin, DateTimeModelMixin, CustomerBase):
    name: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    zip: str
    country: str
