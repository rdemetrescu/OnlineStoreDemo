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
    summary="Get all products",
    description="Retrieves a list of products. Use the **search** parameter to filter products by their names",
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
    summary="Get a product",
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
    summary="Create a new product",
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
    summary="Update a product (full update)",
    description="""Update **all** product fields with new information.

If you need to update only a few fields, please use the **PATCH** method.""",
)
async def full_update_product(
    product_update: ProductCreateUpdate,
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    updated_product = await products_repo.update_product(
        product_id=product_id, product_update=product_update, patching=False
    )
    if updated_product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return updated_product


@router.patch(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    name="products:partial-update-product",
    summary="Update a product (partial update)",
    description="Update only the product fields you need",
)
async def partial_update_product(
    product_update: ProductUpdate,
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    if not product_update.dict(exclude_unset=True):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "empty payload")

    updated_product = await products_repo.update_product(
        product_id=product_id, product_update=product_update, patching=True
    )
    if updated_product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return updated_product


@router.delete(
    "/{product_id}",
    response_model=Product,
    name="products:delete-product-by-id",
    summary="Delete a product",
)
async def delete_product_by_id(
    product_id: PositiveInt,
    products_repo: ProductsRepository = Depends(get_repository(ProductsRepository)),
):
    product = await products_repo.delete_product_by_id(product_id=product_id)

    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product
