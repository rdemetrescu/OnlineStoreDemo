from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic.types import PositiveInt
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.pagination import Pagination
from app.models.customer import Customer, CustomerCreateUpdate, CustomerUpdate


router = APIRouter()


@router.get(
    "/",
    response_model=List[Customer],
    name="customers:get-all-customers",
    summary="Get all customers",
    description="Retrieves a list of customers. Use the **search** parameter to filter customers by their names or emails",
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
    summary="Get a customer",
)
async def get_customer_by_id(
    customer_id: PositiveInt,
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
    summary="Create a new customer",
)
async def create_customer(
    new_customer: CustomerCreateUpdate,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    created_customer = await customers_repo.create_customer(new_customer=new_customer)
    return created_customer


@router.put(
    "/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_200_OK,
    name="customers:full-update-customer",
    summary="Update a customer (full update)",
    description="""Update **all** customer fields with new information.

If you need to update only a few fields, please use the **PATCH** method.""",
)
async def full_update_customer(
    customer_update: CustomerCreateUpdate,
    customer_id: PositiveInt,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    updated_customer = await customers_repo.update_customer(
        customer_id=customer_id, customer_update=customer_update, patching=False
    )
    if updated_customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return updated_customer


@router.patch(
    "/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_200_OK,
    name="customers:partial-update-customer",
    summary="Update a customer (partial update)",
    description="Update only the customer fields you need",
)
async def partial_update_customer(
    customer_update: CustomerUpdate,
    customer_id: PositiveInt,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    if not customer_update.dict(exclude_unset=True):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "empty payload")

    updated_customer = await customers_repo.update_customer(
        customer_id=customer_id, customer_update=customer_update, patching=True
    )
    if updated_customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return updated_customer


@router.delete(
    "/{customer_id}",
    response_model=Customer,
    name="customers:delete-customer-by-id",
    summary="Delete a customer",
)
async def delete_customer_by_id(
    customer_id: PositiveInt,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
):
    customer = await customers_repo.delete_customer_by_id(customer_id=customer_id)

    if customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    return customer
