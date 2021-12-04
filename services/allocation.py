from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

import tables
from database import get_session


class AllocatedPieItemService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> List[tables.AllocatedPieItemModel]:
        return (
            self.session
            .query(tables.AllocatedPieItemModel)
            .all()
        )
