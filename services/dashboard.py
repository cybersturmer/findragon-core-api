from eod import EodHistoricalData
from fastapi import (
    Depends
)
from sqlalchemy.orm import Session

from database import get_session
from settings import settings
from typing import TypedDict


class AssetTotalStats(TypedDict):
    id: int
    code: str
    price: float
    amount: int
    total_purchase: float
    total_market_price: float


class Dashboard:
    def __init__(self, orm_session: Session = Depends(get_session)):
        self.orm_session = orm_session

    def get_total_stats(self):
        # Check if this SQL works for Postgres / Aurora
        # @todo only for current portfolio and maybe user
        transactions_list = \
            self.orm_session \
            .execute(
                "SELECT portfolio_assets.id, portfolio_assets.ticker || '.' || portfolio_assets.exchange as code, "
                "SUM(portfolio_transactions.amount_change) AS amount, "
                "SUM(portfolio_transactions.cost_change) AS total_purchase "
                "FROM portfolio_transactions, portfolio_assets "
                "WHERE portfolio_assets.id == portfolio_transactions.asset_id "
                "GROUP BY portfolio_transactions.asset_id"
            )

        asset_query_list = []
        mapping_list = {}
        response = {}
        for row in transactions_list:
            _asset_id, _code, _amount, _total_purchase = row
            asset = AssetTotalStats(
                id=_asset_id,
                code=_code,
                price=0.0,
                amount=_amount,
                total_purchase=_total_purchase,
                total_market_price=0.0
            )

            mapping_list[_code] = _asset_id

            asset_query_list.append(_code)

            response[_asset_id] = asset

        separator = ','
        asset_query = separator.join(asset_query_list)

        client = EodHistoricalData(settings.eod.api_token)
        eod_response = client.get_prices_live(asset_query)

        eod_response_wrapped = eod_response if type(eod_response) == list else [eod_response]

        eod_data_for_asset: dict
        for eod_data_for_asset in eod_response_wrapped:
            _code = eod_data_for_asset['code']
            _price = float(eod_data_for_asset['previousClose'])

            _asset_id = mapping_list[_code]

            response[_asset_id]['price'] = _price
            response[_asset_id]['total_market_price'] = _price * response[_asset_id]['amount']

        return response

    def get_total_income_stats(self):
        pass
