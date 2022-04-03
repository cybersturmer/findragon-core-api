from fastapi import (
    APIRouter,
    Depends
)

from services.dashboard import Dashboard

router = APIRouter(
    prefix='/dashboard'
)


@router.get('/total_cost_stats')
async def get_total_market_price(
        service: Dashboard = Depends()
):
    return service.get_total_stats()
