from typing import List

from fastapi import APIRouter, Depends, Response, status

from models import schemas
from services.portfolio import Portfolio

router = APIRouter(
    prefix='/portfolios'
)


@router.get('/', response_model=List[schemas.PortfolioGet])
async def get_portfolios(
        service: Portfolio = Depends()
):
    return service.get_list()


@router.post('/', response_model=schemas.PortfolioCreate)
async def create_portfolio(
        data: schemas.PortfolioCreate,
        service: Portfolio = Depends()
):
    return service.create(
        data
    )


@router.get('/{item_id}', response_model=schemas.PortfolioGet)
async def get_portfolio(
        item_id: int,
        service: Portfolio = Depends()
):
    return service.get(
        item_id
    )


@router.put('/{item_id}', response_model=schemas.PortfolioUpdate)
async def update_portfolio(
        item_id: int,
        data: schemas.PortfolioUpdate,
        service: Portfolio = Depends()
):
    return service.update(
        item_id,
        data
    )


@router.delete('/{item_id}')
async def delete_portfolio(
        item_id: int,
        service: Portfolio = Depends()
):
    service.delete(
        item_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
