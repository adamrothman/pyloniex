# -*- coding: utf-8 -*-
from pytest import fixture

from pyloniex import PoloniexPublicAPI


@fixture(scope='session')
def public():
    return PoloniexPublicAPI()


def test_return_ticker(public):
    response = public.return_ticker()
    assert isinstance(response, dict)
    assert len(response) > 0


def test_return_24h_volume(public):
    response = public.return_24h_volume()
    assert isinstance(response, dict)
    assert len(response) > 0


def test_return_order_book(public):
    response = public.return_order_book()
    assert isinstance(response, dict)
    assert len(response) > 0

    response = public.return_order_book(currency_pair='BTC_ETH', depth=4)
    assert isinstance(response, dict)
    assert len(response) > 0


def test_return_trade_history(public):
    response = public.return_trade_history(currency_pair='BTC_ETH')
    assert isinstance(response, list)
    assert len(response) == 200

    response = public.return_trade_history(
        currency_pair='BTC_ETH',
        start=1504634397,
        end=1504648622,
    )
    assert isinstance(response, list)
    assert len(response) == 8308


def test_return_chart_data(public):
    response = public.return_chart_data(
        currency_pair='BTC_ETH',
        period=1800,
        start=1504634397,
        end=1504648622,
    )
    assert isinstance(response, list)
    assert len(response) == 8


def test_return_currencies(public):
    response = public.return_currencies()
    assert isinstance(response, dict)
    assert len(response) > 0


def return_loan_orders(public):
    response = public.return_loan_orders(currency='BTC')
    assert isinstance(response, dict)
    assert len(response) > 0
