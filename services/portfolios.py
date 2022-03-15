from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import tables

from models.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate
)

from database import get_session


class Portfolio:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, item_id: int) -> tables.Portfolio:
        portfolio = (
            self.session
                .query(tables.Portfolio)
                .filter_by(id=item_id)
                .first()
        )

        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return portfolio

    def get_list(self) -> List[tables.Portfolio]:
        return (
            self.session
            .query(tables.Portfolio)
            .all()
        )

    def create(self, data: PortfolioCreate) -> tables.Portfolio:
        portfolio = tables.Portfolio(**data.dict())

        self.session.add(portfolio)
        self.session.commit()

        return portfolio

    def get(self, item_id: int) -> tables.Portfolio:
        return self._get(item_id=item_id)

    def update(self, item_id: int, data: PortfolioUpdate) -> tables.Portfolio:
        portfolio = self._get(item_id=item_id)

        for field, value in data:
            setattr(portfolio, field, value)

        self.session.commit()

        return portfolio

    def delete(self, item_id: int):
        portfolio = self._get(item_id=item_id)

        self.session.delete(portfolio)
        self.session.commit()
