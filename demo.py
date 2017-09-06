# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from time import time

from pyloniex import PoloniexPrivateAPI


def main(key, secret):
    polo = PoloniexPrivateAPI(key=key, secret=secret)

    print('returnBalances')
    response = polo.return_balances()
    print(response)
    print()

    print('returnCompleteBalances')
    response = polo.return_complete_balances()
    print(response)
    print()

    print('returnDepositAddresses')
    response = polo.return_deposit_addresses()
    print(response)
    print()

    print('returnDepositsWithdrawals')
    response = polo.return_deposits_withdrawals(start=0, end=int(time()))
    print(response)
    print()

    print('returnOpenOrders')
    response = polo.return_open_orders()
    print(response)
    print()

    print('returnTradeHistory')
    response = polo.return_trade_history()
    print(response)
    print()

    print('returnFeeInfo')
    response = polo.return_fee_info()
    print(response)
    print()

    print('returnAvailableAccountBalances')
    response = polo.return_available_account_balances()
    print(response)
    print()

    print('returnTradableBalances')
    response = polo.return_tradable_balances()
    print(response)
    print()

    print('returnMarginAccountSummary')
    response = polo.return_margin_account_summary()
    print(response)
    print()

    print('returnOpenLoanOffers')
    response = polo.return_open_loan_offers()
    print(response)
    print()

    print('returnActiveLoans')
    response = polo.return_active_loans()
    print(response)
    print()

    print('returnLendingHistory')
    response = polo.return_lending_history(start=0, end=int(time()))
    print(response)
    print()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('key', type=str, help='Poloniex API key')
    parser.add_argument('secret', type=str, help='Poloniex API secret')
    args = parser.parse_args()

    main(args.key, args.secret)
