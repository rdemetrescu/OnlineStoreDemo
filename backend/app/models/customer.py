from typing import Optional

from pydantic import Field, EmailStr

from app.models.core import BaseModel, DateTimeModelMixin, IDModelMixin

price_validation = Field(..., ge=0)


class CustomerBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]


class CustomerCreate(CustomerBase):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    zip: str
    country: str


class CustomerUpdate(CustomerBase):
    first_name: str
    last_name: str
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
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    zip: str
    country: str
