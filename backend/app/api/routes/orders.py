from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic.types import PositiveInt
from starlette import status

from app.api.dependencies.repositories import get_repository

from app.db.repositories.orders import OrdersRepository
from app.models.pagination import Pagination
from app.models.order import OrderWithItems, OrderCreateUpdate, OrderUpdate, Order
from app.models.order_item import OrderItemCreateUpdate, OrderItemUpdate, OrderItem

router = APIRouter()


@router.get(
    "/",
    response_model=List[Order],
    name="orders:get-all-orders",
    summary="Get all orders",
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
    summary="Get an order",
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
    summary="Create a new order",
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
    description="""Update **all** order fields with new information. **WARNING**: this operation will replace all previous order items with the news items.

If you need to update only a few fields, please use the **PATCH** method.""",
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
    summary="Update an order (partial update)",
    description="Update only the order fields you need",
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
    summary="Delete an order",
)
async def delete_order_by_id(
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order = await orders_repo.delete_order_by_id(order_id=order_id)

    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order


# ==============================================
# ORDER ITEMS
# ==============================================


@router.get(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItem,
    name="orders:get-order-item-by-id",
    summary="Get an order item",
)
async def get_order_item_by_id(
    order_id: PositiveInt,
    order_item_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order_item = await orders_repo.get_order_item_by_id(
        order_id=order_id, order_item_id=order_item_id
    )
    if order_item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "OrderItem not found")
    return order_item


@router.get(
    "/{order_id}/items",
    response_model=List[OrderItem],
    name="orders:get-all-order-items",
    summary="Get all order items",
)
async def get_all_order_items(
    order_id: PositiveInt,
    pagination: Pagination = Depends(),
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):

    orders = await orders_repo.get_all_order_items(
        order_id=order_id, pagination=pagination
    )
    return orders


@router.post(
    "/{order_id}/items",
    response_model=OrderItem,
    status_code=status.HTTP_201_CREATED,
    name="orders:create-order-item",
    summary="Create a new order item",
)
async def create_order_item(
    order_id: PositiveInt,
    new_order_item: OrderItemCreateUpdate,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    created_order = await orders_repo.create_order_item(
        order_id=order_id, new_order_item=new_order_item
    )
    return created_order


@router.put(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItem,
    status_code=status.HTTP_200_OK,
    name="orders:full-update-order-item",
    summary="Update an order item (full update)",
)
async def full_update_order_item(
    order_id: PositiveInt,
    order_item_id: PositiveInt,
    order_item_update: OrderItemCreateUpdate,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    updated_order_item = await orders_repo.update_order_item(
        order_id=order_id,
        order_item_id=order_item_id,
        order_item_update=order_item_update,
        patching=False,
    )
    return updated_order_item


@router.patch(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItem,
    status_code=status.HTTP_200_OK,
    name="orders:partial-update-order-item",
    summary="Upate an order item",
)
async def partial_update_order_item(
    order_id: PositiveInt,
    order_item_id: PositiveInt,
    order_item_update: OrderItemUpdate,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    # raise Exception(order_update.dict(exclude_unset=True))
    if not order_item_update.dict(exclude_unset=True):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "empty payload")

    updated_order_item = await orders_repo.update_order_item(
        order_id=order_id,
        order_item_id=order_item_id,
        order_item_update=order_item_update,
        patching=True,
    )

    return updated_order_item


@router.delete(
    "/{order_id}/items/{order_item_id}",
    response_model=OrderItem,
    name="orders:delete-order-item-by-id",
    summary="Delete an order item",
)
async def delete_order_item_by_id(
    order_id: PositiveInt,
    order_item_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order_item = await orders_repo.delete_order_item_by_id(
        order_id=order_id, order_item_id=order_item_id
    )

    if order_item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "OrderItem not found")
    return order_item


@router.delete(
    "/{order_id}/items",
    response_model=Order,
    name="orders:delete-all-order-items",
    summary="Delete an order items",
)
async def delete_order_items(
    order_id: PositiveInt,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
):
    order = await orders_repo.delete_order_items(order_id=order_id)

    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order
