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

from app.db.repositories.customers import CustomersRepository
from app.models.customer import CustomerCreate, CustomerInDB, CustomerUpdate

from .utils import fake_email_generator


@pytest.fixture
async def test_customer(db: Database) -> CustomerInDB:
    customer_repo = CustomersRepository(db)

    return await customer_repo.create_customer(
        new_customer=CustomerCreate(
            first_name="fake customer first_name [A]",
            last_name="fake customer last_name [A]",
            email=fake_email_generator(),
            phone="fake customer phone [A]",
            street="fake customer street [A]",
            city="fake customer city [A]",
            state="fake customer state [A]",
            zip="fake customer zip [A]",
            country="fake customer country [A]",
        )
    )


@pytest.fixture
async def test_10_customers(db: Database) -> List[CustomerInDB]:
    customer_repo = CustomersRepository(db)

    return [
        await customer_repo.create_customer(
            new_customer=CustomerCreate(
                first_name=f"fake customer first_name [B] - {x}",
                last_name=f"fake customer last_name [B] - {x}",
                email=fake_email_generator(),
                phone=f"fake customer phone [B] - {x}",
                street=f"fake customer street [B] - {x}",
                city=f"fake customer city [B] - {x}",
                state=f"fake customer state [B] - {x}",
                zip=f"fake customer zip [B] - {x}",
                country=f"fake customer country [B] - {x}",
            )
        )
        for x in range(1, 11)
    ]


VALID_NEW_CUSTOMERS = (
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
)


INVALID_NEW_CUSTOMERS = (
    dict(
        # empty info
    ),
    # dict(
    #     first_name="test customer first_name",
    #     last_name="test customer last_name",
    #     email="INVALID email",
    #     phone="test customer phone",
    #     street="test customer street",
    #     city="test customer city",
    #     state="test customer state",
    #     zip="test customer zip",
    #     country="test customer country",
    # ),
    dict(
        # first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        # last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        # email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        # phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        # street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        # city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        # state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        # zip="test customer zip",
        country="test customer country",
    ),
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        # country="test customer country",
    ),
)


INVALID_CUSTOMERS_UPDATE = INVALID_NEW_CUSTOMERS


VALID_CUSTOMERS_UPDATE = (
    dict(
        first_name="test customer first_name",
        last_name="test customer last_name",
        email=fake_email_generator(),
        phone="test customer phone",
        street="test customer street",
        city="test customer city",
        state="test customer state",
        zip="test customer zip",
        country="test customer country",
    ),
)


class TestCreateCustomer:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_NEW_CUSTOMERS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload
    ):
        r = await client.post(
            app.url_path_for("customers:create-customer"), json=payload
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_NEW_CUSTOMERS)
    async def test_valid_input_create_customer(
        self, app: FastAPI, client: AsyncClient, payload
    ):
        r = await client.post(
            app.url_path_for("customers:create-customer"),
            json=payload,
        )
        assert r.status_code == HTTP_201_CREATED, r.text

        # we have at least those 3 fields that come from the database
        assert set(["id", "created_at", "updated_at"]).issubset(
            set(r.json().keys()) - set(payload.keys())
        )

        created_customer = CustomerCreate(**r.json())
        assert created_customer.dict() == CustomerCreate(**payload).dict(), r.text


class TestUpdateCustomer:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_CUSTOMERS_UPDATE)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.put(
            app.url_path_for(
                "customers:update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_CUSTOMERS_UPDATE)
    async def test_valid_input_update_customer(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.put(
            app.url_path_for(
                "customers:update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_200_OK, r.text

        assert test_customer.id == r.json()["id"]

        updated_customer = CustomerUpdate(**r.json())
        assert updated_customer.dict() == CustomerUpdate(**payload).dict(), r.text


class TestGetCustomer:
    @pytest.mark.asyncio
    async def test_get_customer_by_id(
        self, app: FastAPI, client: AsyncClient, test_customer: CustomerInDB
    ):

        r = await client.get(
            app.url_path_for(
                "customers:get-customer-by-id", customer_id=str(test_customer.id)
            )
        )
        assert r.status_code == HTTP_200_OK
        customer = CustomerInDB(**r.json())
        assert customer.id == test_customer.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # customer does not exist  :)
        ),
    )
    async def test_get_customer_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.get(
            app.url_path_for("customers:get-customer-by-id", customer_id=wrong_id)
        )
        assert r.status_code == expected_status

    @pytest.mark.asyncio
    async def test_get_customers(
        self, app: FastAPI, client: AsyncClient, test_10_customers: List[CustomerInDB]
    ):

        r = await client.get(app.url_path_for("customers:get-all-customers"))

        assert r.status_code == HTTP_200_OK
        assert len(r.json()) >= len(test_10_customers)

    @pytest.mark.asyncio
    async def test_get_customers_pagination(
        self, app: FastAPI, client: AsyncClient, test_10_customers: List[CustomerInDB]
    ):
        # pagination without offset
        r1 = await client.get(
            app.url_path_for("customers:get-all-customers"), params=dict(limit=4)
        )
        assert r1.status_code == HTTP_200_OK
        assert len(r1.json()) == 4

        # pagination without offset
        r2 = await client.get(
            app.url_path_for("customers:get-all-customers"),
            params=dict(limit=4, skip=2),
        )
        assert r2.status_code == HTTP_200_OK
        assert len(r2.json()) == 4
        assert r1.json()[0]["id"] != r2.json()[0]["id"]
        assert r1.json()[1]["id"] != r2.json()[0]["id"]
        assert r1.json()[2]["id"] == r2.json()[0]["id"]

    @pytest.mark.asyncio
    async def test_get_customers_search(
        self, app: FastAPI, client: AsyncClient, test_10_customers: List[CustomerInDB]
    ):
        r1 = await client.get(
            app.url_path_for("customers:get-all-customers"), params=dict(limit=1000)
        )
        assert r1.status_code == HTTP_200_OK

        r2 = await client.get(
            app.url_path_for("customers:get-all-customers"),
            params=dict(search="[B] - 1", limit=1000),
        )
        assert r2.status_code == HTTP_200_OK
        assert 0 < len(r2.json()) < len(r1.json())

        r3 = await client.get(
            app.url_path_for("customers:get-all-customers"),
            params=dict(search="this customer shouldn't exist", limit=1000),
        )
        assert r3.status_code == HTTP_200_OK
        assert r3.json() == []


class TestDeleteCustomer:
    @pytest.mark.asyncio
    async def test_delete_customer_by_id(
        self, app: FastAPI, client: AsyncClient, test_customer: CustomerInDB
    ):

        r = await client.delete(
            app.url_path_for(
                "customers:delete-customer-by-id", customer_id=str(test_customer.id)
            )
        )
        assert r.status_code == HTTP_200_OK
        customer = CustomerInDB(**r.json())
        assert customer.id == test_customer.id

        r = await client.get(
            app.url_path_for(
                "customers:delete-customer-by-id", customer_id=str(test_customer.id)
            )
        )

        # Customer shouldn't be found anymore
        assert r.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_id, expected_status",
        (
            (" ", 422),
            ("0", 422),
            ("987654321", 404),  # customer does not exist  :)
        ),
    )
    async def test_delete_customer_by_id_with_wrong_id(
        self, app: FastAPI, client: AsyncClient, wrong_id: str, expected_status: int
    ):
        r = await client.delete(
            app.url_path_for("customers:delete-customer-by-id", customer_id=wrong_id)
        )
        assert r.status_code == expected_status
