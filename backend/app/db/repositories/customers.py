from typing import List, Optional
from fastapi.exceptions import HTTPException

from sqlalchemy import select, or_, and_
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.db.repositories.base import BaseRepository
from app.db.tables.customers import customers_table
from app.models.pagination import Pagination
from app.models.customer import (
    CustomerCreate,
    CustomerInDB,
    CustomerUpdate,
)  # , CustomerUpdate


class CustomersRepository(BaseRepository):
    """ "
    All database actions associated with the Customer resource
    """

    async def get_all_customers(
        self, *, search: str = None, pagination: Pagination
    ) -> Optional[List[CustomerInDB]]:
        query = select([customers_table])
        if search:
            query = query.where(
                or_(
                    customers_table.c.email == search,
                    customers_table.c.name.ilike(f"%{search}%"),
                )
            )

        query = query.limit(pagination.limit).offset(pagination.skip)
        customers = await self.db.fetch_all(query=query)
        return [CustomerInDB(**customer) for customer in customers]

    async def get_customer_by_id(self, *, customer_id: int) -> Optional[CustomerInDB]:
        customer = await self.db.fetch_one(
            query=select([customers_table]).where(customers_table.c.id == customer_id)
        )

        if not customer is None:
            return CustomerInDB(**customer)

    async def create_customer(self, *, new_customer: CustomerCreate) -> CustomerInDB:
        query_values = new_customer.dict()

        async with self.db.transaction():
            existing = await self.db.fetch_one(
                query=select([customers_table]).where(
                    customers_table.c.email == new_customer.email
                )
            )
            if existing is not None:
                raise HTTPException(
                    HTTP_422_UNPROCESSABLE_ENTITY,
                    "There is already a customer using this email",
                )

            customer = await self.db.fetch_one(
                query=customers_table.insert().returning(*customers_table.columns),
                values=query_values,
            )

            return CustomerInDB(**customer)

    async def update_customer(
        self, *, customer_id: int, customer_update: CustomerUpdate
    ) -> Optional[CustomerInDB]:
        customer = await self.get_customer_by_id(customer_id=customer_id)

        if customer is None:
            return

        query_values = customer.copy(
            update=customer_update.dict(exclude_unset=True)
        ).dict()

        async with self.db.transaction():
            existing = await self.db.fetch_one(
                query=select([customers_table]).where(
                    and_(
                        customers_table.c.email == customer.email,
                        customers_table.c.id != customer.id,
                    )
                )
            )
            if existing is not None:
                raise HTTPException(
                    HTTP_422_UNPROCESSABLE_ENTITY,
                    "There is already a customer using this email",
                )

            customer = await self.db.fetch_one(
                query=customers_table.update()
                .where(customers_table.c.id == customer_id)
                .returning(*customers_table.columns),
                values=query_values,
            )

            return CustomerInDB(**customer)

    async def delete_customer_by_id(
        self, *, customer_id: int
    ) -> Optional[CustomerInDB]:
        customer = await self.db.fetch_one(
            query=select([customers_table]).where(customers_table.c.id == customer_id)
        )

        if customer is None:
            return

        # Apply validations for customer deletion

        await self.db.fetch_one(
            query=customers_table.delete().where(customers_table.c.id == customer_id)
        )

        return CustomerInDB(**customer)
