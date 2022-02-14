from typing import List
from fastapi import APIRouter, Depends, Response, status
from models import schemas
from services.transactions import Transaction

router = APIRouter(
    prefix='/transactions'
)

@router.get('/', response_model=List[schemas.TransactionBase])
async def get_transactions(
        service: Transaction = Depends()
):
    return service.get_list()


@router.post('/', response_model=schemas.TransactionGet)
async def create_transaction(
        data: schemas.TransactionCreate,
        service: Transaction = Depends()
):
    return service.create(
        data
    )


@router.get('/{key}', response_model=schemas.TransactionBase)
async def get_transaction(
        key: int,
        service: Transaction = Depends()
):
    return service.get(
        key
    )


@router.put('/{key}', response_model=schemas.TransactionBase)
async def update_transaction(
        key: int,
        data: schemas.TransactionBase,
        service: Transaction = Depends()
):
    return service.update(
        key,
        data
    )


@router.delete('/{key}', response_model=schemas.TransactionBase)
async def delete_transaction(
        key: int,
        data: schemas.TransactionBase,
        service: Transaction = Depends()
):
    return service.delete(
        key
    )
