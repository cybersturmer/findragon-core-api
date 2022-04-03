from typing import List

from fastapi import (
    APIRouter,
    Depends
)

from models.schemas.stats import StatsAssets
from services.stats import Stats

router = APIRouter(
    prefix='/stats'
)


@router.get('/assets', response_model=List[StatsAssets])
async def get_assets_stats(
        service: Stats = Depends()
):
    return service.get_assets_stats()
