from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import tables, schemas

from sqlalchemy_utils import Currency


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

    def create(self, data: schemas.AssetCreate) -> tables.PortfolioAsset:
        data_as_dict = data.dict()

        currency = Currency(
            data_as_dict['currency']
        )

        data_as_dict['currency'] = currency

        asset = tables.PortfolioAsset(**data_as_dict)

        self.orm_session.add(asset)
        self.orm_session.commit()

        return asset

    def delete(self, key: int):
        asset = self._get(key=key)

        self.orm_session.delete(asset)
        self.orm_session.commit()
