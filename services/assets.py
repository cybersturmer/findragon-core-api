from typing import List

from fastapi import Depends, HTTPException, status, File
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database import get_session
from models import tables

from libs.transactions_master import TransactionsMaster

from models.schemas.asset import (
    AssetCreate
)


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

    def get(
            self,
            key: int
    ) -> tables.PortfolioAsset:
        return self._get(key)

    def get_list(self) -> List[dict]:
        transactions: List[tables.PortfolioTransaction] = (
            self.orm_session
            .query(tables.PortfolioTransaction)
            .order_by(tables.PortfolioTransaction.date)
            .all()
        )

        asset_base_cache_list: List[tables.PortfolioAssetBaseCache] = (
            self.orm_session
            .query(tables.PortfolioAssetBaseCache)
            .filter_by(
                manual=True
            )
            .all()
        )

        assets_list: List[tables.PortfolioAsset] = (
            self.orm_session
            .query(tables.PortfolioAsset)
            .all()
        )

        result = []
        _related_cache = None

        asset: tables.PortfolioAsset
        for asset in assets_list:
            try:
                _related_transactions = [
                    transaction_element
                    for transaction_element
                    in transactions
                    if transaction_element.asset == asset
                ]

                _related_cache = [
                    cache
                    for cache
                    in asset_base_cache_list
                    if cache.manual is True
                ].pop()

                transaction_master = TransactionsMaster(_related_transactions)

                _amount_change = transaction_master.calculate_purchase_amount()
                _cost_change = transaction_master.calculate_purchase_cost(_amount_change)
                _avg_price = transaction_master.calculate_average_price()

            except IndexError:
                _amount_change = 0
                _cost_change = 0

                _avg_price = 0

            if _related_cache is None:
                _title = f'{asset.ticker}.{asset.exchange}'
                _description = ''
            else:
                _title = _related_cache.title
                _description = _related_cache.description

            result.append(
                {
                    'id':               asset.id,
                    'ticker':           asset.ticker,
                    'exchange':         asset.exchange,
                    'title':            _title,
                    'description':      _description,
                    'amount_change':    _amount_change,
                    'cost_change':      _cost_change,
                    'avg_price':        _avg_price
                }
            )

        return result

    def create(self, data: AssetCreate) -> tables.PortfolioAsset:
        data_as_dict = data.dict()

        asset = tables.PortfolioAsset(**data_as_dict)

        self.orm_session.add(asset)
        self.orm_session.commit()

        return asset

    def import_xlsx(self, file: File):
        # @todo Move it to transactions.
        pass

    def delete(self, key: int):
        asset = self._get(key=key)

        self.orm_session.delete(asset)
        self.orm_session.commit()
