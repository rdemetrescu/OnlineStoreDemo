from typing import List

import pytest
from databases import Database
from faker import Faker

from app.db.repositories.customers import CustomersRepository
from app.models.customer import CustomerCreateUpdate, CustomerInDB

fake = Faker()


@pytest.fixture
async def test_customer(db: Database) -> CustomerInDB:
    customer_repo = CustomersRepository(db)

    return await customer_repo.create_customer(
        new_customer=CustomerCreateUpdate(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zip=fake.zipcode(),
            country=fake.country(),
        )
    )


@pytest.fixture
async def test_10_customers(db: Database) -> List[CustomerInDB]:
    customer_repo = CustomersRepository(db)

    return [
        await customer_repo.create_customer(
            new_customer=CustomerCreateUpdate(
                name=f"{fake.name()} - {x}",
                email=fake.email(),
                phone=fake.phone_number(),
                street=fake.street_address(),
                city=fake.city(),
                state=fake.street_address(),
                zip=fake.zipcode(),
                country=fake.country(),
            )
        )
        for x in range(1, 11)
    ]


VALID_NEW_CUSTOMERS = (
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
)


INVALID_NEW_CUSTOMERS = (
    dict(
        # empty info
    ),
    dict(
        name=fake.name(),
        email="INVALID email",
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        # name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        # email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        # phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        # street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        # city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        # state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        # zip=fake.zipcode(),
        country=fake.country(),
    ),
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        # country=fake.country(),
    ),
)


VALID_FULL_UPDATE_CUSTOMERS = (
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
)


INVALID_FULL_UPDATE_CUSTOMERS = INVALID_NEW_CUSTOMERS

VALID_PARTIAL_UPDATE_CUSTOMERS = (
    dict(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        street=fake.street_address(),
    ),
    dict(
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
)

INVALID_PARTIAL_UPDATE_CUSTOMERS = (
    dict(
        # empty info
    ),
    dict(
        name=fake.name(),
        email="INVALID email",
        phone=fake.phone_number(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.city(),
        zip=fake.zipcode(),
        country=fake.country(),
    ),
)
