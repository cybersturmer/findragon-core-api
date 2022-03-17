from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import tables

from models.schemas.allocation import (
    PortfolioAllocationCreate,
    PortfolioAllocationUpdate
)

from database import get_session
from models.enums import AllocationType


class Allocation:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def _get(self, key: int) -> tables.PortfolioAllocation:
        allocation = (
            self.orm_session
                .query(tables.PortfolioAllocation)
                .filter_by(id=key)
                .first()
        )

        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return allocation

    def get_list(self) -> List[tables.PortfolioAllocation]:
        return (
            self.orm_session
                .query(tables.PortfolioAllocation)
                .all()
        )

    def create(self, data: PortfolioAllocationCreate) -> tables.PortfolioAllocation:
        allocation_data = data.dict()

        ticker = allocation_data.pop('ticker')
        exchange = allocation_data.pop('exchange')

        allocation_type = allocation_data['type']
        portfolio_id = allocation_data['portfolio_id']

        if allocation_type == AllocationType.ASSET:
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
                asset = tables.PortfolioAsset(
                    **dict(
                        ticker=ticker,
                        exchange=exchange,
                        portfolio_id=portfolio_id
                    )
                )

                self.orm_session.add(asset)
                self.orm_session.commit()

            allocation_data['asset_id'] = asset.id

        allocation = tables.PortfolioAllocation(**allocation_data)

        if allocation.parent_id is not None:
            parent = self._get(allocation.parent_id)
            # @todo What if parent does not exists

            allocation.portfolio_ratio = parent.portfolio_ratio * allocation.category_ratio / 100 ** 2
        else:
            allocation.portfolio_ratio = allocation.category_ratio

        self.orm_session.add(allocation)
        self.orm_session.commit()

        return allocation

    def get(self, key) -> tables.PortfolioAllocation:
        return self._get(key=key)

    def update(self, key: int, data: PortfolioAllocationUpdate) -> tables.PortfolioAllocation:
        allocation_data = data.dict()

        allocation = self._get(key=key)

        """ 
        We can change only category_ratio
        Portfolio ratio is calculated by parent and """
        allocation.category_ratio = allocation_data.pop('category_ratio')

        if allocation.parent_id is not None:
            parent = self._get(allocation.parent_id)
            allocation.portfolio_ratio = parent.portfolio_ratio * allocation.category_ratio / 100 ** 2
        else:
            allocation.portfolio_ratio = allocation.category_ratio

        self.orm_session.commit()

        return allocation

    def delete(self, key: int) -> None:
        allocation = self._get(key=key)
        self.orm_session.delete(allocation)
        self.orm_session.commit()
