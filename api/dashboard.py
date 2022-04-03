from fastapi import (
    APIRouter,
    Depends
)

from services.dashboard import Dashboard

router = APIRouter(
    prefix='/dashboard'
)


@router.get('/assets_stats')
async def get_assets_stats(
        service: Dashboard = Depends()
):
    return service.get_assets_stats()
