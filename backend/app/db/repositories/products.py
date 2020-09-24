from typing import List, Optional

from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.tables.products import products_table
from app.models.pagination import Pagination
from app.models.product import ProductCreate, ProductInDB  # , ProductUpdate


class ProductsRepository(BaseRepository):
    """ "
    All database actions associated with the Product resource
    """

    async def get_all_products(
        self, *, search: str = None, pagination: Pagination
    ) -> Optional[List[ProductInDB]]:
        query = select([products_table])
        if search:
            query = query.where(products_table.c.name.ilike(f"%{search}%"))

        query = query.limit(pagination.limit).offset(pagination.skip)
        products = await self.db.fetch_all(query=query)
        return [ProductInDB(**product) for product in products]

    async def get_product_by_id(self, *, product_id: int) -> Optional[ProductInDB]:
        product = await self.db.fetch_one(
            query=select([products_table]).where(products_table.c.id == product_id)
        )

        if not product is None:
            return ProductInDB(**product)

    async def create_product(self, *, new_product: ProductCreate) -> ProductInDB:
        query_values = new_product.dict()

        async with self.db.transaction():
            product = await self.db.fetch_one(
                query=products_table.insert().returning(*products_table.columns),
                values=query_values,
            )

            return ProductInDB(**product)
