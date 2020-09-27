from typing import Mapping, Optional, List, Union

from fastapi import status, HTTPException
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from starlette.responses import HTMLResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.db.repositories.base import BaseRepository
from app.db.tables.orders import orders_table
from app.db.tables.orders_item import order_items_table
from app.models.order import (
    OrderCreateUpdate,
    OrderInDB,
    OrderUpdate,
    OrderWithItemsInDB,
)
from app.models.pagination import Pagination
from app.utils import dict_include_prefix, dict_remove_prefix


SQL_INSERT_ORDER_ITEMS = """
    insert into order_items (
        order_id,
        product_id,
        product_name,
        price,
        qty,
        total
    )
    select
        :order_id,
        p.id as product_id,
        p.name as product_name,
        p.price,
        cast(:qty as integer),
        p.price * cast(:qty as integer) as total
    from
        products as p
    where
        p.id = :product_id
    returning
        id,
        order_id,
        product_id,
        product_name,
        price,
        qty,
        total,
        created_at,
        updated_at
    """


class OrdersRepository(BaseRepository):
    """ "
    All database actions associated with the Order resource
    """

    async def get_all_orders(
        self, *, pagination: Pagination
    ) -> Optional[List[OrderInDB]]:
        query = select([orders_table])
        query = query.limit(pagination.limit).offset(pagination.skip)
        orders = await self.db.fetch_all(query=query)
        return [
            OrderInDB(**self.adapt_order_flatten_to_model(order)) for order in orders
        ]

    async def get_order_by_id(self, *, order_id: int) -> Optional[OrderInDB]:
        order = await self.db.fetch_one(
            query=select([orders_table]).where(orders_table.c.id == order_id)
        )

        if not order is None:
            return OrderInDB(**self.adapt_order_flatten_to_model(order))

    async def create_order(self, *, new_order: OrderCreateUpdate) -> OrderWithItemsInDB:
        query_values = self.adapt_order_model_to_flatten(new_order)
        query_values["total"] = 0

        async with self.db.transaction():
            order_id = await self.db.fetch_val(
                query=orders_table.insert().returning(orders_table.c.id),
                values=query_values,
            )

            # TODO: turn the code below into a few SQLs for better performance
            # right now we're doing a ugly loop against the items

            items = []

            for item in new_order.items:
                item_db = await self.db.fetch_one(
                    query=SQL_INSERT_ORDER_ITEMS,
                    values=dict(
                        order_id=order_id, product_id=item.product_id, qty=item.qty
                    ),
                )

                if item_db is None:
                    raise HTTPException(
                        status.HTTP_422_UNPROCESSABLE_ENTITY,
                        f"There is no product with id: {item.product_id}",
                    )

                items.append(item_db)

            await self.update_order_total(order_id)
            order = await self.db.fetch_one(
                query=select([orders_table]).where(orders_table.c.id == order_id)
            )

            if order is None:
                raise Exception("Something went really wrong")

            return OrderWithItemsInDB(
                items=items,
                **self.adapt_order_flatten_to_model(order),
            )

    async def update_order(
        self,
        *,
        order_id: int,
        order_update: Union[OrderCreateUpdate, OrderUpdate],
        patching: bool,
    ) -> Optional[Union[OrderWithItemsInDB, OrderInDB]]:

        if isinstance(order_update, OrderCreateUpdate):
            assert patching is False
        if isinstance(order_update, OrderUpdate):
            assert patching is True

        order = await self.get_order_by_id(order_id=order_id)
        items = []

        if order is None:
            return

        query_values = self.adapt_order_model_to_flatten(
            order_update, exclude_unset=patching
        )

        if not patching:
            query_values["total"] = 0

        # raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, query_values)

        async with self.db.transaction():
            order_id = await self.db.fetch_val(
                query=orders_table.update()
                .where(orders_table.c.id == order_id)
                .returning(orders_table.c.id),
                values=query_values,
            )

            if not patching:
                await self.db.execute(
                    query=order_items_table.delete().where(
                        order_items_table.c.order_id == order_id
                    )
                )

            if isinstance(order_update, OrderCreateUpdate):

                for item in order_update.items:
                    item_db = await self.db.fetch_one(
                        query=SQL_INSERT_ORDER_ITEMS,
                        values=dict(
                            order_id=order_id, product_id=item.product_id, qty=item.qty
                        ),
                    )

                    if item_db is None:
                        raise HTTPException(
                            status.HTTP_422_UNPROCESSABLE_ENTITY,
                            f"There is no product with id: {item.product_id}",
                        )

                    items.append(item_db)

                await self.update_order_total(order_id)

            order = await self.db.fetch_one(
                query=select([orders_table]).where(orders_table.c.id == order_id)
            )

            if order is None:
                raise Exception("Something went really wrong here")

            if isinstance(order_update, OrderCreateUpdate):
                return OrderWithItemsInDB(
                    items=items, **self.adapt_order_flatten_to_model(order)
                )

            return OrderInDB(**self.adapt_order_flatten_to_model(order))

    async def delete_order_by_id(self, *, order_id: int) -> Optional[OrderInDB]:
        order = await self.db.fetch_one(
            query=select([orders_table]).where(orders_table.c.id == order_id)
        )

        if order is None:
            return

        # Apply validations for order deletion
        async with self.db.transaction():

            await self.db.execute(
                query=order_items_table.delete().where(
                    order_items_table.c.order_id == order_id
                )
            )
            await self.db.fetch_one(
                query=orders_table.delete().where(orders_table.c.id == order_id)
            )

            return OrderInDB(**self.adapt_order_flatten_to_model(order))

    def adapt_order_model_to_flatten(
        self, order: Union[OrderCreateUpdate, OrderUpdate], exclude_unset: bool = False
    ):
        """
        Convert nested dict structure to a flatten dict (only billing and shipping addresses)
        """
        flatten = dict(
            **order.dict(exclude={"billing_address", "shipping_address", "items"}),
            **dict_include_prefix(
                order.dict(
                    include={"billing_address"}, exclude_unset=exclude_unset
                ).get("billing_address", {}),
                "billing_",
            ),
            **dict_include_prefix(
                order.dict(
                    include={"shipping_address"}, exclude_unset=exclude_unset
                ).get("shipping_address", {}),
                "shipping_",
            ),
        )
        return flatten

    def adapt_order_flatten_to_model(self, flatten: Mapping):
        model = {
            k: v
            for k, v in flatten.items()
            if k in ("id", "total", "created_at", "updated_at")
        }

        aux = dict_remove_prefix(flatten, "billing_")
        if aux:
            model["billing_address"] = aux

        aux = dict_remove_prefix(flatten, "shipping_")
        if aux:
            model["shipping_address"] = aux

        return model

    async def update_order_total(self, order_id):
        await self.db.execute(
            query="""
        update orders set
            total = (
                select sum(it.total)
                from order_items as it
                where it.order_id = orders.id
            )
        where
            id = :order_id
        """,
            values=dict(order_id=order_id),
        )
