from typing import List

from fastapi import APIRouter, Depends, Response, status

from models import schemas
from services.assets import Asset


router = APIRouter(
    prefix='/assets'
)


@router.get('/', response_model=List[schemas.AssetGet])
async def get_assets(
        service: Asset = Depends()
):
    return service.get_list()


@router.get('/{key}', response_model=schemas.AssetGet)
async def get_asset(
        key: int,
        service: Asset = Depends()
):
    return service.get(
        key
    )
