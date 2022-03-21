from fastapi import (
    APIRouter,
    Depends
)

from services.dashboard import Dashboard

router = APIRouter(
    prefix='/dashboard'
)


@router.get('/total_purchase')
async def get_total_purchase(
        service: Dashboard = Depends()
):
    return service.get_total_purchase()