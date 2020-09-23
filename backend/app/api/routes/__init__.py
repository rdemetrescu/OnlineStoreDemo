from fastapi import APIRouter
from app.api.routes import products


router = APIRouter()
router.include_router(products.router, prefix="/products", tags=["Products"])
