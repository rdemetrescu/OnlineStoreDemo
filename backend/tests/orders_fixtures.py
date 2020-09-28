from tests.products_fixtures import test_10_products
from typing import List

import pytest
from databases import Database
from faker import Faker

from app.db.repositories.orders import OrdersRepository
from app.models.order import OrderCreateUpdate, OrderInDB, OrderWithItemsInDB

fake = Faker()


@pytest.fixture
async def test_order(db: Database, test_10_products) -> OrderWithItemsInDB:
    order_repo = OrdersRepository(db)

    return await order_repo.create_order(
        new_order=OrderCreateUpdate(
            billing_address=dict(
                street=fake.street_address(),
                city=fake.city(),
                state=fake.city(),
                zip=fake.zipcode(),
                country=fake.country(),
            ),
            shipping_address=dict(
                street=fake.street_address(),
                city=fake.city(),
                state=fake.city(),
                zip=fake.zipcode(),
                country=fake.country(),
            ),
            items=[
                dict(product_id=test_10_products[0].id, qty=17),
                dict(product_id=test_10_products[1].id, qty=18),
                dict(product_id=test_10_products[2].id, qty=330),
                dict(product_id=test_10_products[3].id, qty=1),
                dict(product_id=test_10_products[4].id, qty=14),
                dict(product_id=test_10_products[5].id, qty=45),
            ],
        )
    )


@pytest.fixture
async def test_10_orders(db: Database) -> List[OrderInDB]:
    order_repo = OrdersRepository(db)

    return [
        await order_repo.create_order(
            new_order=OrderCreateUpdate(
                billing_address=dict(
                    street=fake.street_address(),
                    city=fake.city(),
                    state=fake.city(),
                    zip=fake.zipcode(),
                    country=fake.country(),
                ),
                shipping_address=dict(
                    street=fake.street_address(),
                    city=fake.city(),
                    state=fake.city(),
                    zip=fake.zipcode(),
                    country=fake.country(),
                ),
                items=[dict(product_id=1, qty=17), dict(product_id=2, qty=30)],
            )
        )
        for _ in range(1, 11)
    ]


VALID_NEW_ORDERS = (
    dict(
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[dict(product_id=1, qty=10), dict(product_id=2, qty=3)],
    ),
)

INVALID_NEW_ORDERS = (
    dict(
        # empty info
    ),
    dict(
        # missing complete billing address
        billing_address=dict(
            street=fake.street_address(),
            # city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[dict(product_id=..., qty=10), dict(product_id=..., qty=3)],
    ),
    dict(
        # missing complete shipping address
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=None,
            country=fake.country(),
        ),
        items=[dict(product_id=..., qty=10), dict(product_id=..., qty=3)],
    ),
    dict(
        # missing items - I
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        # items=[dict(product_id=..., qty=10), dict(product_id=..., qty=3)],
    ),
    dict(
        # missing items - II
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=None,
    ),
    dict(
        # missing complete items (product_id)
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[dict(qty=10), dict(qty=3)],
    ),
    dict(
        # missing complete items (qry)
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[dict(product_id=...), dict(product_id=...)],
    ),
)

VALID_FULL_UPDATE_ORDERS = (
    dict(
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[
            dict(product_id=1, qty=300),
            dict(product_id=3, qty=134),
            dict(product_id=5, qty=1),
        ],
    ),
)

INVALID_FULL_UPDATE_ORDERS = INVALID_NEW_ORDERS

VALID_PARTIAL_UPDATE_ORDERS = (
    dict(
        billing_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        shipping_address=dict(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.city(),
            zip=fake.zipcode(),
            country=fake.country(),
        ),
        items=[
            dict(product_id=1, qty=300),
            dict(product_id=3, qty=134),
            dict(product_id=5, qty=1),
        ],
    ),
)

INVALID_PARTIAL_UPDATE_ORDERS = (
    dict(
        # empty info
    ),
    dict(
        # items are useless here..
        items=[dict(product_id=..., qty=10), dict(product_id=..., qty=3)],
    ),
    # TODO: deal with this failing test
    # dict(
    #     # missing complete shipping address
    #     billing_address=dict(
    #         street=fake.street_address(),
    #         city=fake.city(),
    #         state=fake.city(),
    #         zip=fake.zipcode(),
    #         country=fake.country(),
    #     ),
    #     shipping_address=dict(
    #         street=fake.street_address(),
    #         city=fake.city(),
    #         state=fake.city(),
    #         zip=None,
    #         country=fake.country(),
    #     ),
    #     items=[dict(product_id=..., qty=10), dict(product_id=..., qty=3)],
    # ),
)
