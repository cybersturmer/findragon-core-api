from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    File,
    UploadFile
)

from models.schemas.transaction import (
    TransactionsImportResult
)

from models.schemas.asset import (
    AssetAggregated,
    AssetCreate,
    AssetGet
)

from services.assets import Asset

router = APIRouter(
    prefix='/assets'
)


@router.post('/import',
             response_model=TransactionsImportResult)
async def import_assets(
        service: Asset = Depends(),
        file: UploadFile = File(...)
):
    return service.import_xlsx(file)


@router.get('/',
            response_model=List[AssetAggregated],
            summary='Get the list of assets.')
async def get_assets(service: Asset = Depends()):
    return service.get_list()


@router.get('/{key}',
            response_model=AssetGet,
            description='Get the list of the assets with details.')
async def get_asset(key: int, service: Asset = Depends()):
    return service.get(
        key
    )


@router.post('/',
             response_model=AssetGet,
             description='Create the asset in portfolio.')
async def create_asset(data: AssetCreate, service: Asset = Depends()):
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
