from fastapi import APIRouter

from .allocations import router as allocation_router
from .portfolios import router as portfolio_router
from .assets import router as asset_router
from .transactions import router as transaction_router
from .incomes import router as income_router
from .dashboard import router as dashboard_router


router = APIRouter()

router.include_router(allocation_router)
router.include_router(portfolio_router)
router.include_router(transaction_router)
router.include_router(income_router)
router.include_router(asset_router)
router.include_router(dashboard_router)

