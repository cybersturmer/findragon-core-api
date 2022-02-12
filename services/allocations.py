from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import tables, schemas
from database import get_session


class AllocatedPieSlice:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def _get(self, key: int) -> tables.PortfolioAllocatedPieSlice:
        allocation = (
            self.orm_session
                .query(tables.PortfolioAllocatedPieSlice)
                .filter_by(id=key)
                .first()
        )

        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return allocation

    def get_list(self) -> List[tables.PortfolioAllocatedPieSlice]:
        return (
            self.orm_session
            .query(tables.PortfolioAllocatedPieSlice)
            .filter(tables.PortfolioAllocatedPieSlice.parent_id.is_(None))
            .all()
        )

    def create(self, data: schemas.PortfolioAllocatedPieSliceCreate) -> tables.PortfolioAllocatedPieSlice:
        allocation = tables.PortfolioAllocatedPieSlice(**data.dict())

        if allocation.parent_id is not None:
            parent = self._get(allocation.parent_id)
            allocation.portfolio_ratio = parent.portfolio_ratio * allocation.category_ratio / 100 ** 2
        else:
            allocation.portfolio_ratio = allocation.category_ratio

        self.orm_session.add(allocation)
        self.orm_session.commit()

        return allocation

    def get(self, key) -> tables.PortfolioAllocatedPieSlice:
        return self._get(key=key)

    def update(self, key: int, data: schemas.PortfolioAllocatedPieSliceUpdate) -> tables.PortfolioAllocatedPieSlice:
        allocation = self._get(key=key)

        for field, value in data:
            if value is None:
                continue

            setattr(allocation, field, value)

        self.orm_session.commit()

        return allocation

    def delete(self, key: int) -> None:
        allocation = self._get(key=key)
        self.orm_session.delete(allocation)
        self.orm_session.commit()
