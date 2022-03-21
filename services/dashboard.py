from fastapi import (
    Depends
)

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database import get_session
from models import tables


class Dashboard:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def get_total_purchase(
            self
    ):
        request = (
            self.orm_session
            .query(
                func.sum(tables.PortfolioTransaction.cost_change).label('total_purchase')
            )
            .all()
        ) \
        .pop()

        return {
            "total_purchase": request['total_purchase'] * -1
        }

    def get_total_market_price(self):
        pass

    def get_total_income_stats(self):
        pass
