from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import tables, schemas
from database import get_session


class AllocatedPieSlice:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, item_id: int) -> tables.PortfolioAllocatedPieSlice:
        allocation = (
            self.session
                .query(tables.PortfolioAllocatedPieSlice)
                .filter_by(id=item_id)
                .first()
        )

        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return allocation

    def get_list(self) -> List[tables.PortfolioAllocatedPieSlice]:
        return (
            self.session
            .query(tables.PortfolioAllocatedPieSlice)
            .all()
        )

    def create(self, data: schemas.PortfolioAllocatedPieSliceCreate) -> tables.PortfolioAllocatedPieSlice:
        allocation = tables.PortfolioAllocatedPieSlice(**data.dict())

        self.session.add(allocation)
        self.session.commit()

        return allocation

    def get(self, item_id) -> tables.PortfolioAllocatedPieSlice:
        return self._get(item_id=item_id)

    def update(self, item_id: int, data: schemas.PortfolioAllocatedPieSliceUpdate) -> tables.PortfolioAllocatedPieSlice:
        allocation = self._get(item_id=item_id)

        for field, value in data:
            setattr(allocation, field, value)

        self.session.commit()

        return allocation

    def delete(self, item_id: int):
        allocation = self._get(item_id=item_id)
        self.session.delete(allocation)
        self.session.commit()
