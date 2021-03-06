from typing import List

from fastapi import APIRouter, Depends, Response, status

from models.schemas.portfolio import (
    PortfolioGet,
    PortfolioCreate,
    PortfolioUpdate
)

from services.portfolios import Portfolio

router = APIRouter(
    prefix='/portfolios'
)


@router.get('/', response_model=List[PortfolioGet])
async def get_portfolios(
        service: Portfolio = Depends()
):
    return service.get_list()


@router.post('/', response_model=PortfolioGet)
async def create_portfolio(
        data: PortfolioCreate,
        service: Portfolio = Depends()
):
    """
    Goal_type: 0 - Grow, 1 - Income
    """
    return service.create(
        data
    )


@router.get('/{key}', response_model=PortfolioGet)
async def get_portfolio(
        key: int,
        service: Portfolio = Depends()
):
    return service.get(
        key
    )


@router.put('/{key}', response_model=PortfolioUpdate)
async def update_portfolio(
        key: int,
        data: PortfolioUpdate,
        service: Portfolio = Depends()
):
    return service.update(
        key,
        data
    )


@router.delete('/{key}')
async def delete_portfolio(
        key: int,
        service: Portfolio = Depends()
):
    service.delete(
        key
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
