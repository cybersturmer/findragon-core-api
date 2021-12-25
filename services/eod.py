from typing import Union, Optional

from settings import settings
from fastapi import Depends

from database import get_session as get_orm_session, Session as ORMSession
from request import get_session as get_request_session, requests

from io import StringIO

import pandas as pd
from datetime import datetime

from exceptions import RemoteDataError

EOD_HISTORICAL_DATA_API_KEY_ENV_VAR = "EOD_HISTORICAL_API_KEY"


class EOD:
    def __init__(
            self,
            request_session: requests.Session = Depends(get_request_session),
            orm_session: ORMSession = Depends(get_orm_session)
    ):
        self.base_url = settings.eod.api_url
        self.api_token = settings.eod.api_token

        self.request_session = request_session
        self.orm_session = orm_session

    @staticmethod
    def _prepare_ticker(symbol: str, exchange: str) -> str:
        return f'{symbol}.{exchange}'

    @staticmethod
    def _prepare_datetime(datetime_: datetime) -> Optional[str]:
        if datetime_ is None:
            return datetime_

        return f'{datetime_:"%Y-%m-%d"}'

    @staticmethod
    def get_live_data_endpoint(ticker: str) -> str:
        return f'https://eodhistoricaldata.com/api/real-time/{ticker}'

    def get_live_data(self, tickers_list: list):

        if len(tickers_list) < 1:
            raise AttributeError('Ticker list must contain at least one ticker.')

        payload = {
            'api_token': self.api_token,
            'fmt': 'json'
        }

        if len(tickers_list) > 1:
            payload['s'] = ','.join(tickers_list[1:])

        url = self.get_live_data_endpoint(tickers_list[0])

        request = self.request_session.get(
            url,
            json=payload
        )

        if request.status_code != requests.codes.ok:
            raise RemoteDataError(request.status_code, request.reason)

        return request.json()

    def get_eod_endpoint(self, symbol: str, exchange: str) -> str:
        return f'{self.base_url}/eod/{self._prepare_ticker(symbol, exchange)}'

    def get_end_of_day_data(
            self,
            exchange: str,
            symbol: str,
            start: datetime = None,
            end: datetime = None
    ) -> pd.DataFrame:
        """
        Returns End of Day data for given token (symbol.exchange)
        :param exchange: code, like MCX
        :param symbol: code, like SBER
        :param start: python datetime
        :param end: python datetime
        """

        payload = {
            'api_token': self.api_token,
            'from': self._prepare_datetime(start),
            'to': self._prepare_datetime(end)
        }

        request = self.request_session.get(
            self.get_eod_endpoint(
                symbol=symbol,
                exchange=exchange
            ),
            params=payload
        )

        if request.status_code != requests.codes.ok:
            raise RemoteDataError(request.status_code, request.reason)

        csv_dataframe = pd.read_csv(
            StringIO(request.text),
            engine='python',
            header=0,
            names=['date', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume'],
            sep=',',
            parse_dates=[0],
            index_col=0,
            skipfooter=1
        )

        json_dataframe = csv_dataframe.to_json()

        return json_dataframe
