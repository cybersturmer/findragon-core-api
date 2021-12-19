from typing import List

from fastapi import APIRouter, Depends, Response, status

from models import schemas
from services.allocation import AllocatedPieSlice


router = APIRouter(
    prefix='/allocations'
)


@router.get('/', response_model=List[schemas.PortfolioAllocatedPieSliceGet])
async def get_allocations(
        service: AllocatedPieSlice = Depends()
):
    return service.get_list()


@router.post('/', response_model=schemas.PortfolioAllocatedPieSliceCreate)
async def create_allocation(
        data: schemas.PortfolioAllocatedPieSliceCreate,
        service: AllocatedPieSlice = Depends()
):
    return service.create(
        data
    )


@router.get('/{item_id}', response_model=schemas.PortfolioAllocatedPieSliceGet)
async def get_allocation(
        item_id: int,
        service: AllocatedPieSlice = Depends()
):
    return service.get(
        item_id
    )


@router.patch('/{item_id}', response_model=schemas.PortfolioAllocatedPieSliceGet)
async def update_allocation(
        item_id: int,
        data: schemas.PortfolioAllocatedPieSliceUpdate,
        service: AllocatedPieSlice = Depends()
):
    return service.update(
        item_id,
        data
    )


@router.delete('/{item_id}')
async def delete_allocation(
        item_id: int,
        service: AllocatedPieSlice = Depends()
):
    service.delete(
        item_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
