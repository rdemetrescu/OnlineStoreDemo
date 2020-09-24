from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.pagination import Pagination
from app.models.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[Customer],
    name="customers:get-all-customers",
)
async def get_all_customers(
    search: Optional[str] = None,
    pagination: Pagination = Depends(),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    customers = await customers_repo.get_all_customers(
        search=search, pagination=pagination
    )
    return customers


@router.get(
    "/{customer_id}",
    response_model=Customer,
    name="customers:get-customer-by-id",
)
async def get_customer_by_id(
    customer_id: int = Path(..., gt=0),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    customer = await customers_repo.get_customer_by_id(customer_id=customer_id)
    if customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return customer


@router.post(
    "/",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    name="customers:create-customer",
)
async def create_customer(
    new_customer: CustomerCreate,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    created_customer = await customers_repo.create_customer(new_customer=new_customer)
    return created_customer


@router.put(
    "/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_200_OK,
    name="customers:update-customer",
)
async def update_customer(
    # using CustomerCreate to validate input (required fields) as PUT is used to FULL update
    customer_update: CustomerCreate,
    customer_id: int = Path(..., gt=0),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    payload = CustomerUpdate(**customer_update.dict())
    updated_customer = await customers_repo.update_customer(
        customer_id=customer_id, customer_update=payload
    )
    return updated_customer


@router.patch(
    "/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_200_OK,
    name="customers:partial-update-customer",
)
async def update_customer(
    customer_update: CustomerUpdate,
    customer_id: int = Path(..., gt=0),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    raise NotImplementedError()


@router.delete(
    "/{customer_id}",
    response_model=Customer,
    name="customers:delete-customer-by-id",
)
async def delete_customer_by_id(
    customer_id: int = Path(..., gt=0),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    customer = await customers_repo.delete_customer_by_id(customer_id=customer_id)

    if customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return customer
