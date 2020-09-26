from typing import List

import pytest
from app.db.repositories.products import ProductsRepository
from app.models.product import ProductCreateUpdate, ProductInDB, ProductUpdate
from databases import Database


@pytest.fixture
async def test_product(db: Database) -> ProductInDB:
    product_repo = ProductsRepository(db)

    return await product_repo.create_product(
        new_product=ProductCreateUpdate(
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
            new_product=ProductCreateUpdate(
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

VALID_FULL_UPDATE_PRODUCTS = (
    dict(
        name="test UPDATED product name",
        description="test UPDATED product description",
        available="False",
        price="7123.45",  # as string
    ),
    dict(
        name="test UPDATED product name",
        description=None,
        available="False",  # as string
        price=7123.45,
    ),
    dict(
        name="test UPDATED product name",
        # description="test UPDATED product description",
        description=None,
        available=False,
        price="7123.45",  # as string
    ),
)


INVALID_FULL_UPDATE_PRODUCTS = (
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


VALID_PARTIAL_UPDATE_PRODUCTS = (
    dict(
        name="test product name",
        description="test product description",
    ),
    dict(
        available="True",
        price="123.45",
    ),
)


INVALID_PARTIAL_UPDATE_PRODUCTS = (
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
)
