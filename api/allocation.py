from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models import schemas
from services.allocation import AllocatedPieSlice

router = APIRouter(
    prefix='/allocations'
)


@router.get('/', response_model=List[schemas.PortfolioAllocatedPieSlice])
async def get_allocations(service: AllocatedPieSlice = Depends()):
    return service.get_list()


@router.post('/', response_model=schemas.PortfolioAllocatedPieSlice)
async def post_allocations(service: AllocatedPieSlice = Depends()):
    return service.create_instance()


@router.get('/{item_id}', response_model=schemas.PortfolioAllocatedPieSlice)
async def get_allocation(service: AllocatedPieSlice = Depends()):
    return service.get_instance()


@router.put('/{item_id}', response_model=schemas.PortfolioAllocatedPieSlice)
async def update_allocation(service: AllocatedPieSlice = Depends()):
    return service.update_instance()
