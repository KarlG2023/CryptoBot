#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

def log():
    try:
        if len(sys.argv) != 3:
            exit(84)
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
        polo = Poloniex(api_key, api_secret)
        return polo
    except Exception as e:
        print("Unexpected error:", e)
        exit(84)

# Returns all of your available balances.

def get_balance(poloniex):
    return poloniex.returnBalances()

# Returns your balances sorted by account. You may optionally specify
# the "account" POST parameter if you wish to fetch only the balances of
# one account. Please note that balances in your margin account may not
# be accessible if you have any open margin positions or orders.

def get_available_balance(poloniex, account):
    return poloniex.returnCompleteBalances(account)

# Returns all of your balances, including available balance, balance
# on orders, and the estimated BTC value of your balance. By default,
# this call is limited to your exchange account; set the "account" POST
# parameter to "all" to include your margin and lending accounts.

def get_complete_balance(poloniex, account):
    return poloniex.returnBalances(account)

# If you are enrolled in the maker-taker fee schedule, returns your
# current trading fees and trailing 30-day volume in BTC. This
# information is updated once every 24 hours.

def get_fee(poloniex):
    return poloniex.returnFeeInfo()

# man for the poloniex api

def get_help(poloniex):
    help(poloniex)