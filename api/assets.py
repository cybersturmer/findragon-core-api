from typing import List

from fastapi import APIRouter, Depends, Response, status, Path

from models import schemas
from services.assets import Asset


router = APIRouter(
    prefix='/assets'
)


@router.get('/',
            response_model=List[schemas.AssetGet],
            summary='Get the list of assets.')
async def get_assets(
        service: Asset = Depends()
):
    return service.get_list()


@router.get('/{key}',
            response_model=schemas.AssetGet,
            description='Get the list of the assets with details.')
async def get_asset(
        key: int,
        service: Asset = Depends()
):
    return service.get(
        key
    )


@router.delete('/{key}')
async def delete_asset(
        key: int,
        service: Asset = Depends()
):
    service.delete(
        key
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
