from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import tables


class Asset:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def _get(self, key: int) -> tables.PortfolioAsset:
        asset = (
            self.orm_session
            .query(tables.PortfolioAsset)
            .filter_by(id=key)
            .first()
        )

        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return asset

    def get(self, key: int) -> tables.PortfolioAsset:
        return self._get(key)

    def get_list(self) -> List[tables.PortfolioAsset]:
        return (
            self.orm_session
                .query(tables.PortfolioAsset)
                .all()
        )
