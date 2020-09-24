from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repositories.products import ProductsRepository
from app.models.pagination import Pagination
from app.models.product import Product, ProductCreate

router = APIRouter()


@router.get(
    "/",
    response_model=List[Product],
    name="products:get-all-products",
)
async def get_all_products(
    search: Optional[str] = None,
    pagination: Pagination = Depends(),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    products = await products_repo.get_all_products(
        search=search, pagination=pagination
    )
    return products


@router.get(
    "/{product_id}",
    response_model=Product,
    name="products:get-product-by-id",
)
async def get_product_by_id(
    product_id: int = Path(..., gt=0),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    product = await products_repo.get_product_by_id(product_id=product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product


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
