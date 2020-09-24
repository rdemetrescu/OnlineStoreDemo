from hmac import new
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.product import Product, ProductCreate


VALID_NEW_PRODUCTS = (
    dict(
        name="test product name",
        description="test product description",
        available="True",
        price="123.45",
    ),
    dict(
        name="test product name",
        # description="test product description",
        description=None,
        available="True",
        price=123.45,
    ),
    dict(
        name="test product name",
        # description="test product description",
        description=None,
        available=True,
        price="123.45",
    ),
)

INVALID_NEW_PRODUCTS = (
    dict(),
    dict(
        name="test product name",
        description="test product description",
        available="True",
        price=-123.45,
    ),
    dict(
        name="test product name",
        description="test product description",
        available="invalid bool",
        price="123.45",
    ),
    dict(
        name="test product name",
        description="test product description",
        available="True",
        price="invalid number",
    ),
    dict(
        # name="test product name",
        description="test product description",
        available=True,
        price="123.45",
    ),
    dict(
        name="test product name",
        description="test product description",
        # available=True,
        price=123.45,
    ),
    dict(
        name="test product name",
        description="test product description",
        available=True,
        # price=123.45,
    ),
)


class TestProductsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient):
        res = await client.post(app.url_path_for("products:create-product"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND


class TestCreateProduct:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_NEW_PRODUCTS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload
    ):
        r = await client.request(
            "post", app.url_path_for("products:create-product"), json=payload
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_NEW_PRODUCTS)
    async def test_valid_input_create_product(
        self, app: FastAPI, client: AsyncClient, payload
    ):
        r = await client.post(
            app.url_path_for("products:create-product"),
            json=payload,
        )
        assert r.status_code == HTTP_201_CREATED, r.text

        # we have at least those 3 fields that come from the database
        assert set(["id", "created_at", "updated_at"]).issubset(
            set(r.json().keys()) - set(payload.keys())
        )

        created_product = ProductCreate(**r.json())
        assert created_product.dict() == ProductCreate(**payload).dict(), r.text
