import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.order import OrderWithItemsInDB
from app.models.order_item import OrderItemCreateUpdate, OrderItemInDB
from .orders_fixtures import test_order
from .products_fixtures import test_10_products, test_product


class TestCreateOrderItem:
    """
    Testing POST calls
    """

    # @pytest.mark.asyncio
    # async def test_invalid_input_raises_error(...)
    #     TODO

    @pytest.mark.asyncio
    async def test_valid_input_create_order(
        self, app: FastAPI, client: AsyncClient, test_order, test_10_products
    ):

        payload = dict(product_id=test_10_products[0].id, qty=11)

        r = await client.post(
            app.url_path_for("orders:create-order-item", order_id=test_order.id),
            json=payload,
        )
        assert r.status_code == HTTP_201_CREATED, r.text

        # we have at least those 3 fields that come from the database
        assert set(["id", "created_at", "updated_at"]).issubset(
            set(r.json().keys()) - set(payload.keys())
        )

        created_order_item = OrderItemCreateUpdate(**r.json())
        assert (
            created_order_item.dict() == OrderItemCreateUpdate(**payload).dict()
        ), r.text

        # checking if total changed
        r = await client.get(
            app.url_path_for("orders:get-order-by-id", order_id=str(test_order.id))
        )
        assert r.status_code == HTTP_200_OK

        assert r.json()["total"] > test_order.total > 0


class TestFullUpdateOrderItem:
    """
    Testing PUT calls
    """

    # @pytest.mark.asyncio
    # async def test_invalid_input_raises_error(...):
    #     TODO

    @pytest.mark.asyncio
    async def test_valid_input_create_order(
        self, app: FastAPI, client: AsyncClient, test_order, test_product
    ):
        item_to_be_updated = test_order.items[0]

        payload = dict(product_id=test_product.id, qty=item_to_be_updated.qty + 20)

        r = await client.put(
            app.url_path_for(
                "orders:full-update-order-item",
                order_id=test_order.id,
                order_item_id=item_to_be_updated.id,
            ),
            json=payload,
        )
        assert r.status_code == HTTP_200_OK, r.text

        new_item_total = r.json()["total"]
        updated_order_item = OrderItemCreateUpdate(**r.json())
        assert (
            updated_order_item.dict() == OrderItemCreateUpdate(**payload).dict()
        ), r.text

        # checking if total changed
        r = await client.get(
            app.url_path_for("orders:get-order-by-id", order_id=str(test_order.id))
        )
        assert r.status_code == HTTP_200_OK

        assert r.json()["total"] > 0
        assert r.json()["total"] == (
            test_order.total - item_to_be_updated.total + new_item_total
        )


class TestPartialUpdateOrderItem:
    """
    Testing PATCH calls
    """

    # @pytest.mark.asyncio
    # async def test_invalid_input_raises_error(...):
    #     TODO

    @pytest.mark.asyncio
    async def test_valid_input_update_order(
        self, app: FastAPI, client: AsyncClient, test_order, test_product
    ):
        item_to_be_updated = test_order.items[0]
        payloads = (
            dict(product_id=test_product.id),
            dict(qty=item_to_be_updated.qty + 20),
        )

        for payload in payloads:

            r = await client.patch(
                app.url_path_for(
                    "orders:partial-update-order-item",
                    order_id=test_order.id,
                    order_item_id=item_to_be_updated.id,
                ),
                json=payload,
            )
            assert r.status_code == HTTP_200_OK, r.text

            new_item_total = r.json()["total"]

            # checking if total changed
            r = await client.get(
                app.url_path_for("orders:get-order-by-id", order_id=str(test_order.id))
            )
            assert r.status_code == HTTP_200_OK

            assert r.json()["total"] > 0
            assert r.json()["total"] == (
                test_order.total - item_to_be_updated.total + new_item_total
            )


class TestGetOrderItem:
    """
    Testing GET calls
    """

    @pytest.mark.asyncio
    async def test_get_order_item_by_id(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):

        r = await client.get(
            app.url_path_for(
                "orders:get-order-item-by-id",
                order_id=str(test_order.id),
                order_item_id=str(test_order.items[0].id),
            )
        )
        assert r.status_code == HTTP_200_OK
        order_item = OrderItemInDB(**r.json())
        assert order_item.order_id == test_order.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_order_id, wrong_order_item_id, expected_status",
        (
            ("1", " ", 422),
            ("1", "0", 422),
            ("1", "987654321", 404),  # order_item does not exist  :)
            (" ", "1", 422),
            ("0", "1", 422),
            ("987654321", "1", 404),  # order_item does not exist  :)
        ),
    )
    async def test_get_order_item_by_id_with_wrong_id(
        self,
        app: FastAPI,
        client: AsyncClient,
        wrong_order_id: str,
        wrong_order_item_id: str,
        expected_status: int,
    ):
        r = await client.get(
            app.url_path_for(
                "orders:get-order-item-by-id",
                order_id=str(wrong_order_id),
                order_item_id=str(wrong_order_item_id),
            )
        )
        assert r.status_code == expected_status

    @pytest.mark.asyncio
    async def test_get_order_items(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):

        r = await client.get(
            app.url_path_for("orders:get-all-order-items", order_id=str(test_order.id))
        )

        assert r.status_code == HTTP_200_OK
        assert len(r.json()) >= len(test_order.items) > 0

    @pytest.mark.asyncio
    async def test_get_order_items_pagination(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):
        # pagination without offset
        r1 = await client.get(
            app.url_path_for("orders:get-all-order-items", order_id=str(test_order.id)),
            params=dict(limit=4),
        )
        assert r1.status_code == HTTP_200_OK
        assert len(r1.json()) == 4

        # pagination without offset
        r2 = await client.get(
            app.url_path_for("orders:get-all-order-items", order_id=str(test_order.id)),
            params=dict(limit=4, skip=2),
        )
        assert r2.status_code == HTTP_200_OK
        assert len(r2.json()) == 4
        assert r1.json()[0]["id"] != r2.json()[0]["id"]
        assert r1.json()[1]["id"] != r2.json()[0]["id"]
        assert r1.json()[2]["id"] == r2.json()[0]["id"]


class TestDeleteOrderItem:
    """
    Testing DELETE calls
    """

    @pytest.mark.asyncio
    async def test_delete_order_by_id(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):

        r = await client.delete(
            app.url_path_for(
                "orders:delete-order-item-by-id",
                order_id=str(test_order.id),
                order_item_id=str(test_order.items[0].id),
            )
        )
        assert r.status_code == HTTP_200_OK
        order_item = OrderItemInDB(**r.json())
        assert order_item.id == test_order.items[0].id

        r = await client.get(
            app.url_path_for(
                "orders:get-order-item-by-id",
                order_id=str(test_order.id),
                order_item_id=str(test_order.items[0].id),
            )
        )

        # OrderItem shouldn't be found anymore
        assert r.status_code == HTTP_404_NOT_FOUND

    # @pytest.mark.asyncio
    # async def test_delete_order_by_id_with_wrong_id(...):
    #     TODO
