from typing import List

from fastapi import (
    Depends,
    HTTPException,
    status
)

from database import (
    Session,
    get_session
)

from models import tables

from models.schemas.income import (
    IncomeCreate,
    IncomeUpdate
)


class Income:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def _get(self, key: int) -> tables.PortfolioIncome:
        income = (
            self.orm_session
            .query(tables.PortfolioIncome)
            .filter_by(id=key)
            .first()
        )

        if not income:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return income

    def get(self, key: int) -> tables.PortfolioIncome:
        return self._get(key)

    def get_list(self) -> List[tables.PortfolioIncome]:
        return (
            self.orm_session
            .query(tables.PortfolioIncome)
            .all()
        )

    def create(self, data: IncomeCreate) -> tables.PortfolioIncome:
        income_data = data.dict()

        ticker = income_data.pop('ticker')
        exchange = income_data.pop('exchange')

        portfolio_id = income_data['portfolio_id']

        asset = (
            self.orm_session
            .query(tables.PortfolioAsset)
            .filter_by(
                ticker=ticker,
                exchange=exchange,
                portfolio_id=portfolio_id
            )
            .first()
        )

        if not asset:
            asset = tables.PortfolioIncome(
                **dict(
                    ticker=ticker,
                    exchange=exchange,
                    portfolio_id=portfolio_id
                )
            )

            self.orm_session.add(asset)
            self.orm_session.commit()

        income = tables.PortfolioIncome(**income_data)
        income.asset_id = asset.id

        self.orm_session.add(income)
        self.orm_session.commit()

        return income

    def delete(self, key: int) -> None:
        income = self._get(key=key)

        self.orm_session.delete(income)
        self.orm_session.commit()

    def update(self,
               key: int,
               data: IncomeUpdate) -> tables.PortfolioIncome:

        income = self._get(key=key)

        for field, value in data:
            if value is None:
                continue

            setattr(income, field, value)

        self.orm_session.commit()

        return income