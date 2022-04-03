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

    total_purchase_cost: float
    total_market_price: float

    portfolio_change: float
    portfolio_change_p: float

    change: float
    change_p: float


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
            _asset_id, _code, _amount, _total_purchase_cost = row
            asset = AssetTotalStats(
                id=_asset_id,
                code=_code,
                price=0.0,
                amount=_amount,
                total_purchase_cost=_total_purchase_cost,
                total_market_price=0.0,
                portfolio_change=0.0,
                portfolio_change_p=0.0,
                change=0.0,
                change_p=0.0
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
            _asset_id = mapping_list[_code]

            _price = float(eod_data_for_asset['previousClose'])

            _total_market_price = _price * response[_asset_id]['amount']

            _total_purchase_cost = response[_asset_id]['total_purchase_cost']

            _total_diff = _total_market_price - _total_purchase_cost
            _total_ratio = _total_diff / _total_purchase_cost * 100

            response[_asset_id]['portfolio_change'] = _total_diff
            response[_asset_id]['portfolio_change_p'] = _total_ratio

            response[_asset_id]['price'] = _price

            response[_asset_id]['total_market_price'] = _total_market_price

            response[_asset_id]['change'] = eod_data_for_asset['change']
            response[_asset_id]['change_p'] = eod_data_for_asset['change_p']

        return response

    def get_total_income_stats(self):
        pass
