from typing import List

from fastapi import APIRouter, Depends, Response, status

from models import schemas, tables
from services.assets import Asset

router = APIRouter(
    prefix='/assets'
)


@router.get('/',
            response_model=List[schemas.AssetGet],
            summary='Get the list of assets.')
async def get_assets(service: Asset = Depends()):
    return service.get_list()


@router.get('/{key}',
            response_model=schemas.AssetGet,
            description='Get the list of the assets with details.')
async def get_asset(key: int, service: Asset = Depends()):
    return service.get(
        key
    )


@router.post('/',
             response_model=schemas.AssetGet,
             description='Create the asset in portfolio.')
async def create_asset(data: schemas.AssetCreate, service: Asset = Depends()) -> tables.PortfolioAsset:
    return service.create(
        data
    )


@router.delete('/{key}')
async def delete_asset(key: int, service: Asset = Depends()):
    service.delete(
        key
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
