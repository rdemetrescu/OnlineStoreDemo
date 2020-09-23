import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.product import ProductCreate


@pytest.fixture
def new_product() -> ProductCreate:
    return ProductCreate(
        name="test product name",
        description="test product description",
        available=True,
        price=123.45,
    )


class TestProductsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient):
        res = await client.post(app.url_path_for("products:create-product"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND


class TestCreateProduct:
    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient):
        res = await client.post(app.url_path_for("products:create-product"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_valid_input_create_product(
        self, app: FastAPI, client: AsyncClient, new_product: ProductCreate
    ):
        res = await client.post(
            app.url_path_for("products:create-product"),
            json={"new_product": new_product.dict()},
        )
        assert res.status_code == HTTP_201_CREATED
        created_product = ProductCreate(**res.json())
        assert created_product == new_product
