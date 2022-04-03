from fastapi import (
    APIRouter,
    Depends
)

from models.schemas.dashboard import DashboardAssetsStats
from services.dashboard import Dashboard

router = APIRouter(
    prefix='/dashboard'
)


@router.get('/assets_stats', response_model=DashboardAssetsStats)
async def get_assets_stats(
        service: Dashboard = Depends()
):
    return service.get_assets_stats()
