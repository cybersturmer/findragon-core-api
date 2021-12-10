from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models import schemas
from services.allocation import AllocatedPieSlice

router = APIRouter(
    prefix='/allocations'
)


@router.get('/', response_model=List[schemas.PortfolioAllocatedPieSlice])
async def get_allocations(
        service: AllocatedPieSlice = Depends()
):
    return service.get_list()


@router.post('/', response_model=schemas.PortfolioAllocatedPieSlice)
async def create_allocation(
        data: schemas.PortfolioAllocatedPieSliceCreate,
        service: AllocatedPieSlice = Depends()
):
    return service.create(
        data
    )


@router.get('/{item_id}', response_model=schemas.PortfolioAllocatedPieSlice)
async def get_allocation(
        item_id: int,
        service: AllocatedPieSlice = Depends()
):
    return service.get(
        item_id
    )


@router.put('/{item_id}', response_model=schemas.PortfolioAllocatedPieSlice)
async def update_allocation(
        item_id: int,
        data: schemas.PortfolioAllocatedPieSliceUpdate,
        service: AllocatedPieSlice = Depends()
):
    return service.update(
        item_id,
        data
    )


@router.delete('/{item_id}', response_model=schemas.PortfolioAllocatedPieSlice)
async def delete_allocation(
        item_id: int,
        service: AllocatedPieSlice = Depends()
):
    return service.delete(
        item_id
    )
