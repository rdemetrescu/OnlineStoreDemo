from app.api.routes import customers, products, orders
from fastapi import APIRouter

router = APIRouter()
router.include_router(orders.router, prefix="/orders", tags=["Orders"])
router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(customers.router, prefix="/customers", tags=["Customers"])
