#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

# Returns the 24-hour volume for all markets, plus totals for
# primary currencies.

def get24hVolume(poloniex):
    return poloniex.return24hVolume()

# Returns candlestick chart data. Required GET parameters are
# "currencyPair", "period" (candlestick period in seconds; valid values
# are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end".
# "Start" and "end" are given in UNIX timestamp format and used to
# specify the date range for the data returned.
# example: poloniex.returnChartData(['USDT_BTC'], 86400, start=1605450419, end=1608042419

def get_chart_data(poloniex, currencyPair, period, start, end):
    return poloniex.returnChartData(currencyPair, period, start, end )

# Returns information about currencies.

def getCurrenciesInfo(poloniex):
    return poloniex.returnCurrencies()

# Returns the order book for a given market, as well as a sequence
# number for use with the Push API and an indicator specifying whether
# the market is frozen. You may set currencyPair to "all" to get the
# order books of all markets.

def getOrderBook(poloniex, currencyPair, depth):
    return poloniex.returnOrderBook(currencyPair, depth)

# Returns the ticker for all markets.
# return poloniex.returnTicker()['USDT_BTC'] for specific output

def get_ticker(poloniex):
    return poloniex.returnTicker()