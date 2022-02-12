from typing import List

from fastapi import Depends, HTTPException, status

from database import Session, get_session
from models import tables, schemas
from services import assets


class Transaction:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def _get(self, key: int) -> tables.PortfolioTransaction:
        transaction = (
            self.orm_session
            .query(tables.PortfolioTransaction)
            .filter_by(id=key)
            .first()
        )

        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return transaction

    def get(self, key: int) -> tables.PortfolioTransaction:
        return self._get(key)

    def get_list(self) -> List[tables.PortfolioTransaction]:
        return (
            self.orm_session
            .query(tables.PortfolioTransaction)
            .all()
        )

    def create(self, data: schemas.TransactionBase) -> tables.PortfolioTransaction:
        transaction_data = data.dict()

        ticker = transaction_data.pop('ticker')
        exchange = transaction_data.pop('exchange')

        portfolio_id = transaction_data['portfolio_id']

        asset = (
            self.orm_session
            .query(tables.PortfolioAsset)
            .filter_by(
                ticker=ticker,
                exchange=exchange
            )
            .first()
        )

        # Let's add asset if it not exists yet
        if not asset:
            asset = tables.PortfolioAsset(
                **dict(
                    ticker=ticker,
                    exchange=exchange,
                    portfolio_id=portfolio_id
                )
            )

            self.orm_session.add(asset)
            self.orm_session.commit()

        transaction = tables.PortfolioTransaction(**transaction_data)

        transaction.total_price = transaction.amount * transaction.price

        transaction.imported = False
        transaction.import_id = None

        transaction.asset_id = asset.id

        self.orm_session.add(transaction)
        self.orm_session.commit()

        return transaction

    def delete(self, key: int):
        transaction = self._get(key=key)

        self.orm_session.delete(transaction)
        self.orm_session.commit()

    def update(self,
               key: int,
               data: schemas.TransactionUpdate) -> tables.PortfolioTransaction:

        transaction = self._get(key=key)

        for field, value in data:
            if value is None:
                continue

            setattr(transaction, field, value)

        transaction.total_price = transaction.amount * transaction.price

        transaction.imported = False

        self.orm_session.commit()

        return transaction

