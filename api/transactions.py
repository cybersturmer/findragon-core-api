from typing import List

from fastapi import APIRouter, Depends

from models.schemas.transaction import (
    TransactionGet,
    TransactionCreate,
    TransactionUpdate
)

from services.transactions import Transaction

router = APIRouter(
    prefix='/transactions'
)


@router.get('/', response_model=List[TransactionGet])
async def get_transactions(
        service: Transaction = Depends()
):
    """
    Get all transactions.
    We will filter them in a future by user_id and portfolio
    @todo Filter by user_id
    @todo Filter by portfolio_id
    """
    return service.get_list()


@router.post('/', response_model=TransactionGet)
async def create_transaction(
        data: TransactionCreate,
        service: Transaction = Depends()
):
    """
    Create transaction.
    Transaction is buying / selling asset
    on exactly date with fixed price and commission.
    """
    return service.create(
        data
    )


@router.get('/{key}', response_model=TransactionGet)
async def get_transaction(
        key: int,
        service: Transaction = Depends()
):
    """
    Get transaction by id.
    I don't think we will need it in a future.
    """
    return service.get(
        key
    )


@router.put('/{key}', response_model=TransactionGet)
async def update_transaction(
        key: int,
        data: TransactionUpdate,
        service: Transaction = Depends()
):
    """
    Update transaction by id in
    a case if we were mistaken.
    """
    return service.update(
        key,
        data
    )


@router.delete('/{key}', response_model=TransactionGet)
async def delete_transaction(
        key: int,
        service: Transaction = Depends()
):
    """
    Delete transaction if it's not
    valid / was created by mistake.
    """
    return service.delete(
        key
    )
