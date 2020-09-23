from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status
from app.models.product import ProductCreate, Product
from app.db.repositories.products import ProductsRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_product(
    new_product: ProductCreate = Body(..., embed=True),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    created_product = await products_repo.create_product(new_product=new_product)
    return created_product