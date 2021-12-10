from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from models import tables
from database import get_session


class AllocatedPieSlice:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> List[tables.PortfolioAllocatedPieSlice]:
        return (
            self.session
            .query(tables.PortfolioAllocatedPieSlice)
            .all()
        )

    def create_instance(self) -> tables.PortfolioAllocatedPieSlice:
        pass

    def get_instance(self) -> tables.PortfolioAllocatedPieSlice:
        pass

    def update_instance(self) -> tables.PortfolioAllocatedPieSlice:
        pass
