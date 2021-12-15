from fastapi import APIRouter
from .allocation import router as allocation_router
from .portfolio import router as portfolio_router

router = APIRouter()
router.include_router(allocation_router)
router.include_router(portfolio_router)
