from typing import List

from fastapi import APIRouter, Depends, Response, status

from models.schemas.allocation import (
    PortfolioAllocationGet,
    PortfolioAllocationCreate,
    PortfolioAllocationUpdate
)
from services.allocations import Allocation


router = APIRouter(
    prefix='/allocations'
)


@router.get('/', response_model=List[PortfolioAllocationGet])
async def get_allocations(
        service: Allocation = Depends()
):
    return service.get_list()


@router.post('/', response_model=PortfolioAllocationGet)
async def create_allocation(
        data: PortfolioAllocationCreate,
        service: Allocation = Depends()
):
    """
    Type: 1 - Asset, 2 - Category, 3 - Currency
    """
    return service.create(
        data
    )


@router.get('/{key}', response_model=PortfolioAllocationGet)
async def get_allocation(
        key: int,
        service: Allocation = Depends()
):
    return service.get(
        key
    )


@router.patch('/{key}', response_model=PortfolioAllocationGet)
async def update_allocation(
        key: int,
        data: PortfolioAllocationUpdate,
        service: Allocation = Depends()
):
    return service.update(
        key,
        data
    )


@router.delete('/{key}')
async def delete_allocation(
        key: int,
        service: Allocation = Depends()
):
    service.delete(
        key
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
