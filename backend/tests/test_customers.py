from typing import List

import pytest
from app.models.customer import CustomerCreateUpdate, CustomerInDB, CustomerUpdate
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from .customers_fixtures import (
    INVALID_FULL_UPDATE_CUSTOMERS,
    INVALID_NEW_CUSTOMERS,
    INVALID_PARTIAL_UPDATE_CUSTOMERS,
    VALID_FULL_UPDATE_CUSTOMERS,
    VALID_NEW_CUSTOMERS,
    VALID_PARTIAL_UPDATE_CUSTOMERS,
    test_10_customers,
    test_customer,
)


class TestCreateCustomer:
    """
    Testing POST calls
    """

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

        created_customer = CustomerCreateUpdate(**r.json())
        assert created_customer.dict() == CustomerCreateUpdate(**payload).dict(), r.text


class TestFullUpdateCustomer:
    """
    Testing PUT calls
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_FULL_UPDATE_CUSTOMERS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.put(
            app.url_path_for(
                "customers:full-update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_FULL_UPDATE_CUSTOMERS)
    async def test_valid_input_update_customer(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.put(
            app.url_path_for(
                "customers:full-update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_200_OK, r.text

        assert test_customer.id == r.json()["id"]

        updated_customer = CustomerUpdate(**r.json())
        assert updated_customer.dict() == CustomerUpdate(**payload).dict(), r.text


class TestPartialUpdateCustomer:
    """
    Testing PATCH calls
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", INVALID_PARTIAL_UPDATE_CUSTOMERS)
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.patch(
            app.url_path_for(
                "customers:partial-update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_422_UNPROCESSABLE_ENTITY, r.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload", VALID_PARTIAL_UPDATE_CUSTOMERS)
    async def test_valid_input_partial_update_customer(
        self, app: FastAPI, client: AsyncClient, payload, test_customer: CustomerInDB
    ):
        r = await client.patch(
            app.url_path_for(
                "customers:partial-update-customer", customer_id=str(test_customer.id)
            ),
            json=payload,
        )
        assert r.status_code == HTTP_200_OK, r.text

        assert test_customer.id == r.json()["id"]

        # updated_customer = CustomerUpdate(**r.json())
        # assert updated_customer.dict() == CustomerUpdate(**payload).dict(), r.text


class TestGetCustomer:
    """
    Testing GET calls
    """

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
            params=dict(search=" - 1", limit=1000),
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
    """
    Testing DELETE calls
    """

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
