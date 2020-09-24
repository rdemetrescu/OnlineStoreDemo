from typing import List

import pytest
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.db.repositories.products import ProductsRepository
from app.models.product import ProductCreate, ProductInDB, ProductUpdate


@pytest.fixture
async def test_product(db: Database) -> ProductInDB:
    product_repo = ProductsRepository(db)

    return await product_repo.create_product(
        new_product=ProductCreate(
            name="fake product name [A]",
            description="fake product description [A]",
            available=True,
            price=600,
        )
    )


@pytest.fixture
async def test_10_products(db: Database) -> List[ProductInDB]:
    product_repo = ProductsRepository(db)

    return [
        await product_repo.create_product(
            new_product=ProductCreate(
                name=f"fake product name [B] - {x}",
                description=f"fake product description [B] - {x}",
                available=x % 2,
                price=x * 300,
            )
        )
        for x in range(1, 11)
    ]


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
    dict(
        # empty info
    ),
    dict(
        # price is negative
        name="test product name",
        description="test product description",
        available="True",
        price=-123.45,
    ),
    dict(  # available is invalid boolean
        name="test product name",
        description="test product description",
        available="invalid bool",
        price="123.45",
    ),
    dict(  # price is invalid float
        name="test product name",
        description="test product description",
        available="True",
        price="invalid number",
    ),
    dict(  # name is missing - I
        # name="test product name",
        description="test product description",
        available=True,
        price="123.45",
    ),
    dict(  # name is missing - II
        name=None,
        description="test product description",
        available=True,
        price="123.45",
    ),
    dict(  # available is missing - I
        name="test product name",
        description="test product description",
        # available=True,
        price=123.45,
    ),
    dict(  # available is missing - II
        name="test product name",
        description="test product description",
        available=None,
        price=123.45,
    ),
    dict(  # price is missing - I
        name="test product name",
        description="test product description",
        available=True,
        # price=123.45,
    ),
    dict(  # price is missing - II
        name="test product name",
        description="test product description",
        available=True,
        price=None,
    ),
)

INVALID_PRODUCTS_UPDATE = (
    dict(
        # empty info
    ),
    dict(
        # price is negative
        name="test product name",
        description="test product description",
        available="True",
        price=-123.45,
    ),
    dict(  # available is invalid boolean
        name="test product name",
        description="test product description",
        available="invalid bool",
        price="123.45",
    ),
    dict(  # price is invalid float
        name="test product name",
        description="test product description",
        available="True",
        price="invalid number",
    ),
    dict(  # name is missing - I
        # name="test product name",
        description="test product description",
        available=True,
        price="123.45",
    ),
    dict(  # name is missing - II
        name=None,
        description="test product description",
        available=True,
        price="123.45",
    ),
    dict(  # available is missing - I
        name="test product name",
        description="test product description",
        # available=True,
        price=123.45,
    ),
    dict(  # available is missing - II
        name="test product name",
        description="test product description",
        available=None,
        price=123.45,
    ),
    dict(  # price is missing - I
        name="test product name",
        description="test product description",
        available=True,
        # price=123.45,
    ),
    dict(  # price is missing - II
        name="test product name",
        description="test product description",
        available=True,
        price=None,
    ),
)

VALID_PRODUCTS_UPDATE = (
    dict(
        name="test UPDATED product name",
        description="test UPDATED product description",
        available="False",
        price="7123.45",
    ),
    dict(
        name="test UPDATED product name",
        # description="test UPDATED product description",
        description=None,
        available="False",
        price=7123.45,
    ),
    dict(
        name="test UPDATED product name",
        # description="test UPDATED product description",
        description=None,
        available=False,
        price="7123.45",
    ),
)


class TestCreateProduct:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_NEW_PRODUCTS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload
    ):
        r = await client.post(app.url_path_for("products:create-product"), json=payload)
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


class TestUpdateProduct:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_PRODUCTS_UPDATE)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload, test_product: ProductInDB
    ):
        r = await client.put(
            app.url_path_for(
                "products:update-product", product_id=str(test_product.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_PRODUCTS_UPDATE)
    async def test_valid_input_update_product(
        self, app: FastAPI, client: AsyncClient, payload, test_product: ProductInDB
    ):
        r = await client.put(
            app.url_path_for(
                "products:update-product", product_id=str(test_product.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_200_OK, r.text

        assert test_product.id == r.json()["id"]

        updated_product = ProductUpdate(**r.json())
        assert updated_product.dict() == ProductUpdate(**payload).dict(), r.text


class TestGetProduct:
    @pytest.mark.asyncio
    async def test_get_product_by_id(
        self, app: FastAPI, client: AsyncClient, test_product: ProductInDB
    ):

        r = await client.get(
            app.url_path_for(
                "products:get-product-by-id", product_id=str(test_product.id)
            )
        )
        assert r.status_code == HTTP_200_OK
        product = ProductInDB(**r.json())
        assert product.id == test_product.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # product does not exist  :)
        ),
    )
    async def test_get_product_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.get(
            app.url_path_for("products:get-product-by-id", product_id=wrong_id)
        )
        assert r.status_code == expected_status

    @pytest.mark.asyncio
    async def test_get_products(
        self, app: FastAPI, client: AsyncClient, test_10_products: List[ProductInDB]
    ):

        r = await client.get(app.url_path_for("products:get-all-products"))

        assert r.status_code == HTTP_200_OK
        assert len(r.json()) >= len(test_10_products)

    @pytest.mark.asyncio
    async def test_get_products_pagination(
        self, app: FastAPI, client: AsyncClient, test_10_products: List[ProductInDB]
    ):
        # pagination without offset
        r1 = await client.get(
            app.url_path_for("products:get-all-products"), params=dict(limit=4)
        )
        assert r1.status_code == HTTP_200_OK
        assert len(r1.json()) == 4

        # pagination without offset
        r2 = await client.get(
            app.url_path_for("products:get-all-products"), params=dict(limit=4, skip=2)
        )
        assert r2.status_code == HTTP_200_OK
        assert len(r2.json()) == 4
        assert r1.json()[0]["id"] != r2.json()[0]["id"]
        assert r1.json()[1]["id"] != r2.json()[0]["id"]
        assert r1.json()[2]["id"] == r2.json()[0]["id"]

    @pytest.mark.asyncio
    async def test_get_products_search(
        self, app: FastAPI, client: AsyncClient, test_10_products: List[ProductInDB]
    ):
        r1 = await client.get(
            app.url_path_for("products:get-all-products"), params=dict(limit=1000)
        )
        assert r1.status_code == HTTP_200_OK

        r2 = await client.get(
            app.url_path_for("products:get-all-products"),
            params=dict(search="[B] - 1", limit=1000),
        )
        assert r2.status_code == HTTP_200_OK
        assert 0 < len(r2.json()) < len(r1.json())

        r3 = await client.get(
            app.url_path_for("products:get-all-products"),
            params=dict(search="this product shouldn't exist", limit=1000),
        )
        assert r3.status_code == HTTP_200_OK
        assert r3.json() == []


class TestDeleteProduct:
    @pytest.mark.asyncio
    async def test_delete_product_by_id(
        self, app: FastAPI, client: AsyncClient, test_product: ProductInDB
    ):

        r = await client.delete(
            app.url_path_for(
                "products:delete-product-by-id", product_id=str(test_product.id)
            )
        )
        assert r.status_code == HTTP_200_OK
        product = ProductInDB(**r.json())
        assert product.id == test_product.id

        r = await client.get(
            app.url_path_for(
                "products:delete-product-by-id", product_id=str(test_product.id)
            )
        )

        # Product shouldn't be found anymore
        assert r.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # product does not exist  :)
        ),
    )
    async def test_delete_product_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.delete(
            app.url_path_for("products:delete-product-by-id", product_id=wrong_id)
        )
        assert r.status_code == expected_status
