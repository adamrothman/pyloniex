# -*- coding: utf-8 -*-
from typing import Any
from typing import Dict
from typing import Optional

from pyloniex.api import PoloniexBaseAPI
from pyloniex.api import REQUESTS_PER_SECOND


class PoloniexPublicAPI(PoloniexBaseAPI):

    host = 'https://poloniex.com/public'

    def __init__(
        self,
        *,
        requests_per_second: int = REQUESTS_PER_SECOND,
    ) -> None:
        super().__init__(requests_per_second=requests_per_second)

    # Commands

    def return_ticker(self):
        params = {'command': 'returnTicker'}
        return self.request('GET', type(self).host, params=params)

    def return_24h_volume(self):
        params = {'command': 'return24hVolume'}
        return self.request('GET', type(self).host, params=params)

    def return_order_book(
        self,
        *,
        currency_pair: Optional[str] = None,
        depth: Optional[int] = None,
    ):
        params: Dict[str, Any] = {
            'command': 'returnOrderBook',
            'currencyPair': 'all' if currency_pair is None else currency_pair,
        }
        if depth is not None:
            params['depth'] = depth
        return self.request('GET', type(self).host, params=params)

    def return_trade_history(
        self,
        *,
        currency_pair: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ):
        params: Dict[str, Any] = {
            'command': 'returnTradeHistory',
            'currencyPair': currency_pair,
        }
        if start is not None and end is not None:
            params['start'] = start
            params['end'] = end
        return self.request('GET', type(self).host, params=params)

    def return_chart_data(
        self,
        *,
        currency_pair: str,
        period: int,
        start: int,
        end: int,
    ):
        params = {
            'command': 'returnChartData',
            'currencyPair': currency_pair,
            'period': period,
            'start': start,
            'end': end,
        }
        return self.request('GET', type(self).host, params=params)

    def return_currencies(self):
        params = {
            'command': 'returnCurrencies',
        }
        return self.request('GET', type(self).host, params=params)

    def return_loan_orders(self, *, currency: str):
        params = {
            'command': 'returnLoanOrders',
            'currency': currency,
        }
        return self.request('GET', type(self).host, params=params)
