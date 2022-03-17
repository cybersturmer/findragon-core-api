from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status
)

from models.schemas.income import (
    IncomeGet,
    IncomeCreate,
    IncomeUpdate
)
from services.incomes import Income

router = APIRouter(
    prefix='/income'
)


@router.get('/', response_model=List[IncomeGet])
async def get_incomes(
        service: Income = Depends()
):
    return service.get_list()


@router.post('/', response_model=IncomeGet)
async def create_income(
        data: IncomeCreate,
        service: Income = Depends()
):
    return service.create(
        data
    )


@router.get('/{key}', response_model=IncomeGet)
async def get_income(
        key: int,
        service: Income = Depends()
):
    return service.get(
        key
    )


@router.put('/{key}', response_model=IncomeGet)
async def update_income(
        key: int,
        data: IncomeUpdate,
        service: Income = Depends()
):
    return service.update(
        key,
        data
    )


@router.delete('/{key}', response_model=IncomeGet)
async def delete_income(
        key: int,
        service: Income = Depends()
):
    service.delete(
        key
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
