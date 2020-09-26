from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic.types import PositiveInt
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repositories.products import ProductsRepository
from app.models.pagination import Pagination
from app.models.product import Product, ProductCreateUpdate, ProductUpdate


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
    product_id: PositiveInt,
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
    new_product: ProductCreateUpdate,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    created_product = await products_repo.create_product(new_product=new_product)
    return created_product


@router.put(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    name="products:full-update-product",
)
async def full_update_product(
    # using ProductCreate to validate input (required fields) as PUT is used to FULL update
    product_update: ProductCreateUpdate,
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    updated_product = await products_repo.update_product(
        product_id=product_id, product_update=product_update, patching=False
    )
    return updated_product


@router.patch(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    name="products:partial-update-product",
)
async def partial_update_product(
    product_update: ProductUpdate,
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    # raise Exception(product_update.dict(exclude_unset=True))
    if not product_update.dict(exclude_unset=True):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "empty payload")

    updated_product = await products_repo.update_product(
        product_id=product_id, product_update=product_update, patching=True
    )
    return updated_product


@router.delete(
    "/{product_id}",
    response_model=Product,
    name="products:delete-product-by-id",
)
async def delete_product_by_id(
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    product = await products_repo.delete_product_by_id(product_id=product_id)

    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product
