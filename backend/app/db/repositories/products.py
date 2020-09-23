from app.db.repositories.base import BaseRepository
from app.db.tables.products import products_table
from app.models.product import ProductCreate, ProductInDB  # , ProductUpdate


class ProductsRepository(BaseRepository):
    """ "
    All database actions associated with the Product resource
    """

    async def create_product(self, *, new_product: ProductCreate) -> ProductInDB:
        query_values = new_product.dict()

        async with self.db.transaction():
            product = await self.db.fetch_one(
                query=products_table.insert().returning(*products_table.columns),
                values=query_values,
            )

            return ProductInDB(**product)
