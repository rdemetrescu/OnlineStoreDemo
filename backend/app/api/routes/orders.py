from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic.types import PositiveInt
from starlette import status

from app.api.dependencies.repositories import get_repository

from app.db.repositories.orders import OrdersRepository
from app.models.pagination import Pagination
from app.models.order import OrderWithItems, OrderCreateUpdate, OrderUpdate, Order

router = APIRouter()


@router.get(
    "/",
    response_model=List[Order],
    name="orders:get-all-orders",
)
async def get_all_orders(
    pagination: Pagination = Depends(),
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    orders = await orders_repo.get_all_orders(pagination=pagination)
    return orders


@router.get(
    "/{order_id}",
    response_model=Order,
    name="orders:get-order-by-id",
)
async def get_order_by_id(
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order = await orders_repo.get_order_by_id(order_id=order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order


@router.post(
    "/",
    response_model=OrderWithItems,
    status_code=status.HTTP_201_CREATED,
    name="orders:create-order",
)
async def create_order(
    new_order: OrderCreateUpdate,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    created_order = await orders_repo.create_order(new_order=new_order)
    return created_order


@router.put(
    "/{order_id}",
    response_model=OrderWithItems,
    status_code=status.HTTP_200_OK,
    name="orders:full-update-order",
)
async def full_update_order(
    order_update: OrderCreateUpdate,
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    updated_order = await orders_repo.update_order(
        order_id=order_id, order_update=order_update, patching=False
    )
    return updated_order


@router.patch(
    "/{order_id}",
    response_model=Order,
    status_code=status.HTTP_200_OK,
    name="orders:partial-update-order",
)
async def partial_update_order(
    order_update: OrderUpdate,
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    # raise Exception(order_update.dict(exclude_unset=True))
    if not order_update.dict(exclude_unset=True):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "empty payload")

    updated_order = await orders_repo.update_order(
        order_id=order_id, order_update=order_update, patching=True
    )

    return updated_order


@router.delete(
    "/{order_id}",
    response_model=Order,
    name="orders:delete-order-by-id",
)
async def delete_order_by_id(
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order = await orders_repo.delete_order_by_id(order_id=order_id)

    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order