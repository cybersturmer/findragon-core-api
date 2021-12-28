from typing import List

from fastapi import Depends, HTTPException, status

from database import Session, get_session
from models import tables, schemas


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

    def _create(self, transaction: tables.PortfolioTransaction):
        self.orm_session.add(transaction)
        self.orm_session.commit()

    def create(self, data: schemas.PortfolioT):
        pass

