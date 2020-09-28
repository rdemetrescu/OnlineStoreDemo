import copy
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.order import OrderCreateUpdate, OrderInDB, OrderWithItemsInDB
from .orders_fixtures import (
    INVALID_FULL_UPDATE_ORDERS,
    INVALID_NEW_ORDERS,
    INVALID_PARTIAL_UPDATE_ORDERS,
    VALID_FULL_UPDATE_ORDERS,
    VALID_NEW_ORDERS,
    VALID_PARTIAL_UPDATE_ORDERS,
    test_10_orders,
    test_order,
)
from .products_fixtures import test_10_products


class TestCreateOrder:
    """
    Testing POST calls
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_NEW_ORDERS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, test_10_products, payload
    ):
        payload = copy.deepcopy(payload)
        if payload.get("items"):
            for item, product in zip(payload["items"], test_10_products):
                if item.get("product_id") == ...:
                    item["product_id"] = product.id

        r = await client.post(app.url_path_for("orders:create-order"), json=payload)
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_NEW_ORDERS)
    async def test_valid_input_create_order(
        self, app: FastAPI, client: AsyncClient, payload, test_10_products
    ):
        for item, product in zip(payload["items"], test_10_products):
            if item.get("product_id") == ...:
                item["product_id"] = product.id

        r = await client.post(
            app.url_path_for("orders:create-order"),
            json=payload,
        )
        assert r.status_code == HTTP_201_CREATED, r.text

        # we have at least those 3 fields that come from the database
        assert set(["id", "created_at", "updated_at"]).issubset(
            set(r.json().keys()) - set(payload.keys())
        )

        assert len(r.json()["items"]) == len(payload["items"]) > 0

        created_order = OrderCreateUpdate(**r.json())
        assert created_order.dict() == OrderCreateUpdate(**payload).dict(), r.text

        total = 0
        for item in r.json()["items"]:
            assert item["total"] == round(item["qty"] * item["price"], 2)
            assert item["total"] > 0
            total += item["total"]

        assert r.json()["total"] == round(total, 2) > 0


class TestFullUpdateOrder:
    """
    Testing PUT calls
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_FULL_UPDATE_ORDERS)
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_10_products,
        payload,
        test_order: OrderWithItemsInDB,
    ):
        payload = copy.deepcopy(payload)
        if payload.get("items"):
            for item, product in zip(payload["items"], test_10_products):
                if item.get("product_id") == ...:
                    item["product_id"] = product.id

        r = await client.put(
            app.url_path_for("orders:full-update-order", order_id=str(test_order.id)),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_FULL_UPDATE_ORDERS)
    async def test_valid_input_update_order(
        self,
        app: FastAPI,
        client: AsyncClient,
        payload,
        test_order: OrderWithItemsInDB,
        test_10_products,
    ):
        for item, product in zip(payload["items"], test_10_products):
            if item.get("product_id") == ...:
                item["product_id"] = product.id

        r = await client.put(
            app.url_path_for("orders:full-update-order", order_id=str(test_order.id)),
            json=payload,
        )

        assert r.status_code == HTTP_200_OK

        assert len(r.json()["items"]) == len(payload["items"]) > 0

        total = 0
        for item in r.json()["items"]:
            assert item["total"] == round(item["qty"] * item["price"], 2)
            assert item["total"] > 0
            total += item["total"]

        assert r.json()["total"] == round(total, 2) > 0


class TestPartialUpdateOrder:
    """
    Testing PATCH calls
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_PARTIAL_UPDATE_ORDERS)
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_10_products,
        payload,
        test_order: OrderWithItemsInDB,
    ):
        payload = copy.deepcopy(payload)
        if payload.get("items"):
            for item, product in zip(payload["items"], test_10_products):
                if item.get("product_id") == ...:
                    item["product_id"] = product.id

        r = await client.patch(
            app.url_path_for(
                "orders:partial-update-order", order_id=str(test_order.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_PARTIAL_UPDATE_ORDERS)
    async def test_valid_input_update_order(
        self,
        app: FastAPI,
        client: AsyncClient,
        payload,
        test_order: OrderWithItemsInDB,
    ):
        r = await client.patch(
            app.url_path_for(
                "orders:partial-update-order", order_id=str(test_order.id)
            ),
            json=payload,
        )

        assert r.status_code == HTTP_200_OK

        assert r.json()["total"] == test_order.total > 0


class TestGetOrder:
    """
    Testing GET calls
    """

    @pytest.mark.asyncio
    async def test_get_order_by_id(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):

        r = await client.get(
            app.url_path_for("orders:get-order-by-id", order_id=str(test_order.id))
        )
        assert r.status_code == HTTP_200_OK
        order = OrderInDB(**r.json())
        assert order.id == test_order.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # order does not exist  :)
        ),
    )
    async def test_get_order_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.get(
            app.url_path_for("orders:get-order-by-id", order_id=wrong_id)
        )
        assert r.status_code == expected_status

    @pytest.mark.asyncio
    async def test_get_orders(
        self, app: FastAPI, client: AsyncClient, test_10_orders: List[OrderInDB]
    ):

        r = await client.get(app.url_path_for("orders:get-all-orders"))

        assert r.status_code == HTTP_200_OK
        assert len(r.json()) >= len(test_10_orders) > 0

    @pytest.mark.asyncio
    async def test_get_orders_pagination(
        self, app: FastAPI, client: AsyncClient, test_10_orders: List[OrderInDB]
    ):
        # pagination without offset
        r1 = await client.get(
            app.url_path_for("orders:get-all-orders"), params=dict(limit=4)
        )
        assert r1.status_code == HTTP_200_OK
        assert len(r1.json()) == 4

        # pagination without offset
        r2 = await client.get(
            app.url_path_for("orders:get-all-orders"),
            params=dict(limit=4, skip=2),
        )
        assert r2.status_code == HTTP_200_OK
        assert len(r2.json()) == 4
        assert r1.json()[0]["id"] != r2.json()[0]["id"]
        assert r1.json()[1]["id"] != r2.json()[0]["id"]
        assert r1.json()[2]["id"] == r2.json()[0]["id"]


class TestDeleteOrder:
    """
    Testing DELETE calls
    """

    @pytest.mark.asyncio
    async def test_delete_order_by_id(
        self, app: FastAPI, client: AsyncClient, test_order: OrderWithItemsInDB
    ):

        r = await client.delete(
            app.url_path_for("orders:delete-order-by-id", order_id=str(test_order.id))
        )
        assert r.status_code == HTTP_200_OK
        order = OrderInDB(**r.json())
        assert order.id == test_order.id

        r = await client.get(
            app.url_path_for("orders:delete-order-by-id", order_id=str(test_order.id))
        )

        # Order shouldn't be found anymore
        assert r.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # order does not exist  :)
        ),
    )
    async def test_delete_order_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.delete(
            app.url_path_for("orders:delete-order-by-id", order_id=wrong_id)
        )
        assert r.status_code == expected_status
