# -*- coding: utf-8 -*-
import time
from binascii import hexlify
from typing import Any
from typing import Dict
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.hmac import HMAC
from requests.auth import AuthBase

from pyloniex.api import PoloniexBaseAPI
from pyloniex.api import REQUESTS_PER_SECOND
from pyloniex.constants import OrderType
from pyloniex.utils import protect_floats


class PoloniexAuth(AuthBase):

    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret

    def __call__(self, request):
        hmac = HMAC(self.secret.encode('utf-8'), SHA512(), default_backend())
        hmac.update(request.body.encode('utf-8'))
        signature = hexlify(hmac.finalize())

        request.headers['Key'] = self.key
        request.headers['Sign'] = signature

        return request


class PoloniexPrivateAPI(PoloniexBaseAPI):

    host = 'https://poloniex.com/tradingApi'

    def __init__(
        self,
        *,
        key: str,
        secret: str,
        requests_per_second: int = REQUESTS_PER_SECOND,
    ) -> None:
        super().__init__(requests_per_second=REQUESTS_PER_SECOND)
        self._session.auth = PoloniexAuth(key, secret)  # type: ignore

    @classmethod
    def nonce(cls) -> int:
        """We use the time to generate our nonce values. The actual value must
        be an int and cannot repeat, so we convert to microseconds.
        """
        return int(time.time() * 1000000)

    def private_request(self, params: Dict[str, Any]):
        cls = type(self)
        data = protect_floats(params)
        data['nonce'] = cls.nonce()
        return self.request('POST', cls.host, data=data)

    # Commands

    def return_balances(self):
        params = {
            'command': 'returnBalances',
        }
        return self.private_request(params)

    def return_complete_balances(self, *, account: Optional[str] = None):
        params = {
            'command': 'returnCompleteBalances',
        }
        if account is not None:
            params['account'] = account
        return self.private_request(params)

    def return_deposit_addresses(self):
        params = {
            'command': 'returnDepositAddresses',
        }
        return self.private_request(params)

    def generate_new_address(self, *, currency: str):
        params = {
            'command': 'generateNewAddress',
            'currency': currency,
        }
        return self.private_request(params)

    def return_deposits_withdrawals(self, *, start: int, end: int):
        params = {
            'command': 'returnDepositsWithdrawals',
            'start': start,
            'end': end,
        }
        return self.private_request(params)

    def return_open_orders(self, *, currency_pair: Optional[str] = None):
        params = {
            'command': 'returnOpenOrders',
            'currencyPair': 'all' if currency_pair is None else currency_pair,
        }
        return self.private_request(params)

    def return_trade_history(
        self,
        *,
        currency_pair: Optional[str] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        params: Dict[str, Any] = {
            'command': 'returnTradeHistory',
            'currencyPair': 'all' if currency_pair is None else currency_pair,
        }
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if limit is not None:
            params['limit'] = limit
        return self.private_request(params)

    def return_order_trades(self, *, order_number: int):
        params = {
            'command': 'returnOrderTrades',
            'orderNumber': order_number,
        }
        return self.private_request(params)

    def buy(
        self,
        *,
        currency_pair: str,
        rate: float,
        amount: float,
        order_type: Optional[OrderType] = None,
    ):
        params = {
            'command': 'buy',
            'currencyPair': currency_pair,
            'rate': rate,
            'amount': amount,
        }
        if type is not None:
            params[order_type.value] = 1
        return self.private_request(params)

    def sell(
        self,
        *,
        currency_pair: str,
        rate: float,
        amount: float,
        order_type: Optional[OrderType] = None,
    ):
        params = {
            'command': 'sell',
            'currencyPair': currency_pair,
            'rate': rate,
            'amount': amount,
        }
        if type is not None:
            params[order_type.value] = 1
        return self.private_request(params)

    def cancel_order(self, *, order_number: int):
        params = {
            'command': 'cancelOrder',
            'orderNumber': order_number,
        }
        return self.private_request(params)

    def move_order(
        self,
        *,
        order_number: int,
        rate: float,
        amount: Optional[float] = None,
        order_type: Optional[OrderType] = None,
    ):
        params = {
            'command': 'moveOrder',
            'orderNumber': order_number,
            'rate': rate,
        }
        if amount is not None:
            params['amount'] = amount
        if order_type is not None:
            params[order_type.value] = 1
        return self.private_request(params)

    def withdraw(
        self,
        *,
        currency: str,
        amount: float,
        address: str,
        payment_id: Optional[str] = None,
    ):
        params = {
            'command': 'withdraw',
            'amount': amount,
            'address': address,
        }
        if payment_id is not None:
            params['paymentId'] = payment_id
        return self.private_request(params)

    def return_fee_info(self):
        params = {
            'command': 'returnFeeInfo',
        }
        return self.private_request(params)

    def return_available_account_balances(
        self,
        *,
        account: Optional[str] = None,
    ):
        params = {
            'command': 'returnAvailableAccountBalances',
        }
        if account is not None:
            params['account'] = account
        return self.private_request(params)

    def return_tradable_balances(self):
        params = {
            'command': 'returnTradableBalances',
        }
        return self.private_request(params)

    def transfer_balance(
        self,
        *,
        currency: str,
        amount: float,
        from_account: str,
        to_account: str,
    ):
        params = {
            'command': 'transferBalance',
            'currency': currency,
            'fromAccount': from_account,
            'toAccount': to_account,
        }
        return self.private_request(params)

    def return_margin_account_summary(self):
        params = {
            'command': 'returnMarginAccountSummary',
        }
        return self.private_request(params)

    def margin_buy(
        self,
        *,
        currency_pair: str,
        rate: float,
        amount: float,
        lending_rate: Optional[float] = None,
    ):
        params = {
            'command': 'marginBuy',
            'currencyPair': currency_pair,
            'rate': rate,
            'amount': amount,
        }
        if lending_rate is not None:
            params['lendingRate'] = lending_rate
        return self.private_request(params)

    def margin_sell(
        self,
        *,
        currency_pair: str,
        rate: float,
        amount: float,
        lending_rate: Optional[float] = None,
    ):
        params = {
            'command': 'marginSell',
            'currencyPair': currency_pair,
            'rate': rate,
            'amount': amount,
        }
        if lending_rate is not None:
            params['lendingRate'] = lending_rate
        return self.private_request(params)

    def get_margin_position(self, *, currency_pair: Optional[str] = None):
        params = {
            'command': 'getMarginPosition',
            'currencyPair': 'all' if currency_pair is None else currency_pair,
        }
        return self.private_request(params)

    def close_margin_position(self, *, currency_pair: str):
        params = {
            'command': 'closeMarginPosition',
            'currencyPair': currency_pair,
        }
        return self.private_request(params)

    def create_loan_offer(
        self,
        *,
        currency: str,
        amount: float,
        duration: float,
        auto_renew: bool,
        lending_rate: float,
    ):
        params = {
            'command': 'createLoanOffer',
            'currency': currency,
            'amount': amount,
            'duration': duration,
            'autoRenew': 1 if auto_renew is True else 0,
            'lendingRate': lending_rate,
        }
        return self.private_request(params)

    def cancel_loan_offer(self, *, order_number: int):
        params = {
            'command': 'cancelLoanOffer',
            'orderNumber': order_number,
        }
        return self.private_request(params)

    def return_open_loan_offers(self):
        params = {
            'command': 'returnOpenLoanOffers',
        }
        return self.private_request(params)

    def return_active_loans(self):
        params = {
            'command': 'returnActiveLoans',
        }
        return self.private_request(params)

    def return_lending_history(
        self,
        *,
        start: int,
        end: int,
        limit: Optional[int] = None,
    ):
        params = {
            'command': 'returnLendingHistory',
            'start': start,
            'end': end,
        }
        if limit is not None:
            params['limit'] = limit
        return self.private_request(params)

    def toggle_auto_renew(self, *, order_number: int):
        params = {
            'command': 'toggleAutoRenew',
            'orderNumber': order_number,
        }
        return self.private_request(params)
