from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status
)

from models import schemas
from services.income import Income

router = APIRouter(
    prefix='/income'
)


@router.get('/', response_model=List[schemas.IncomeGet])
async def get_incomes(
        service: Income = Depends()
):
    return service.get_list()


@router.post('/', response_model=schemas.IncomeGet)
async def create_income(
        data: schemas.IncomeCreate,
        service: Income = Depends()
):
    return service.create(
        data
    )


@router.get('/{key}', response_model=schemas.IncomeGet)
async def get_income(
        key: int,
        service: Income = Depends()
):
    return service.get(
        key
    )


@router.put('/{key}', response_model=schemas.IncomeGet)
async def update_income(
        key: int,
        data: schemas.IncomeUpdate,
        service: Income = Depends()
):
    return service.update(
        key,
        data
    )


@router.delete('/{key}', response_model=schemas.IncomeGet)
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
