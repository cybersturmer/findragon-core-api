from typing import List

from fastapi import Depends, HTTPException, status, File
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database import get_session
from models import tables

from models.schemas.asset import (
    AssetCreate
)

from models.enums import TransactionType


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
        transaction_aggregation = (
            self.orm_session
            .query(
                tables.PortfolioTransaction.asset_id,
                tables.PortfolioTransaction.type,
                func.sum(tables.PortfolioTransaction.amount).label('amount'),
                func.sum(tables.PortfolioTransaction.total_price).label('total_price')
            )
            .group_by(
                tables.PortfolioTransaction.type,
                tables.PortfolioTransaction.asset_id
            )
            .all()
        )

        assets_list = (
            self.orm_session
            .query(tables.PortfolioAsset)
            .all()
        )

        result = []

        asset: tables.PortfolioAsset
        for asset in assets_list:

            try:
                related_buy_transaction = [
                    transaction_element
                    for transaction_element
                    in transaction_aggregation
                    if transaction_element['type'] == TransactionType.BUY
                    and transaction_element['asset_id'] == asset.id].pop()
            except IndexError:
                related_buy_transaction = {
                    'type': TransactionType.BUY,
                    'asset_id': asset.id,
                    'amount': 0,
                    'total_price': 0
                }

            try:
                related_sell_transaction = [
                    transaction_element
                    for transaction_element
                    in transaction_aggregation
                    if transaction_element['type'] == TransactionType.SELL
                    and transaction_element['asset_id'] == asset.id].pop()
            except IndexError:
                related_sell_transaction = {
                    'type': TransactionType.SELL,
                    'asset_id': asset.id,
                    'amount': 0,
                    'total_price': 0
                }

            _amount = related_buy_transaction['amount'] - related_sell_transaction['amount']

            _price = related_buy_transaction['total_price'] - related_sell_transaction['total_price'] \
                if _amount > 0 \
                else None

            _avg_price = round(_price / _amount, 2) \
                if _amount > 0 \
                else None

            result.append(
                {
                    'id': asset.id,
                    'ticker': asset.ticker,
                    'exchange': asset.exchange,
                    'description': asset.description,
                    'amount': _amount,
                    'total_price': _price,
                    'avg_price': _avg_price
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
