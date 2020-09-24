from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repositories.products import ProductsRepository
from app.models.pagination import Pagination
from app.models.product import Product, ProductCreate, ProductUpdate

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


@router.put(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    name="products:update-product",
)
async def update_product(
    # using ProductCreate to validate input (required fields) as PUT is used to FULL update
    product_update: ProductCreate,
    product_id: int = Path(..., gt=0),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    payload = ProductUpdate(**product_update.dict())
    updated_product = await products_repo.update_product(
        product_id=product_id, product_update=payload
    )
    return updated_product


@router.patch(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    name="products:partial-update-product",
)
async def update_product(
    product_update: ProductUpdate,
    product_id: int = Path(..., gt=0),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    raise NotImplementedError()


@router.delete(
    "/{product_id}",
    response_model=Product,
    name="products:delete-product-by-id",
)
async def delete_product_by_id(
    product_id: int = Path(..., gt=0),
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    product = await products_repo.delete_product_by_id(product_id=product_id)

    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product
