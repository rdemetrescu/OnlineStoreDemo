from typing import List

from fastapi import APIRouter, Depends, Body
from starlette import status

from app.api.dependencies.database import get_repository
from app.db.repositories.products import ProductsRepository
from app.models.product import Product, ProductCreate

router = APIRouter()


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    name="products:create-product",
)
async def create_product(
    new_product: ProductCreate,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    created_product = await products_repo.create_product(new_product=new_product)
    return created_product
