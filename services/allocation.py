from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from models.tables import PortfolioAllocatedPieItemModel
from database import get_session


class AllocatedPieItemService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> List[PortfolioAllocatedPieItemModel]:
        return (
            self.session
            .query(PortfolioAllocatedPieItemModel)
            .all()
        )
