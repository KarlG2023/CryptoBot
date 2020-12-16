#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

# If successful, the method will return the order number
# You may optionally set "fillOrKill", "immediateOrCancel", "postOnly"
# to 1. A fill-or-kill order will either fill in its entirety or be
# completely aborted. An immediate-or-cancel order can be partially or
# completely filled, but any portion of the order that cannot be filled
# immediately will be canceled rather than left on the order book.
# A post-only order will only be placed if no portion of it fills
# immediately; this guarantees you will never pay the taker fee on any
# part of the order that fills.

def buy(poloniex, currencyPair, rate, amount, fillOrKill, immediateOrCancel, postOnly):
    return poloniex.buy(currencyPair, rate, amount, fillOrKill, immediateOrCancel, postOnly)

# Places a sell order in a given market. Parameters and output are
# the same as for the buy method.

def sell(poloniex, currencyPair, rate, amount, fillOrKill, immediateOrCancel, postOnly):
    return poloniex.sell(currencyPair, rate, amount, fillOrKill, immediateOrCancel, postOnly)

# Cancels an order you have placed in a given market. Required POST parameter is "orderNumber".

def cancelOrder(poloniex, orderNumber):
    return poloniex.cancelOrder(orderNumber)

# Cancels an order and places a new one of the same type in a single
# atomic transaction, meaning either both operations will succeed or both
# will fail. Required POST parameters are "orderNumber" and "rate"; you
# may optionally specify "amount" if you wish to change the amount of
# the new order. "postOnly" or "immediateOrCancel" may be specified for
# exchange orders, but will have no effect on margin orders.

def moveOrder(poloniex, orderNumber, rate, amount, postOnly, immediateOrCancel):
    return poloniex.moveOrder(orderNumber, rate, amount, postOnly, immediateOrCancel)

# Returns your open orders for a given market, specified by the
# "currencyPair" POST parameter, e.g. "BTC_XCP". Set "currencyPair" to
# "all" to return open orders for all markets.

def getOpenOrders(poloniex, currencyPair):
    return poloniex.returnOpenOrders(currencyPair)

# Returns all trades involving a given order, specified by the
# "orderNumber" POST parameter. If no trades for the order have occurred
# or you specify an order that does not belong to you, you will receive
# an error.

def getOrderTrades(poloniex, orderNumber):
    return poloniex.returnOrderTrades(orderNumber)

# Returns your trade history for a given market, specified by the
# "currencyPair" POST parameter. You may specify "all" as the
# currencyPair to receive your trade history for all markets. You may
# optionally specify a range via "start" and/or "end" POST parameters,
# given in UNIX timestamp format; if you do not specify a range, it will
# be limited to one day.

def getTradeHistory(poloniex, currencyPair, start, end, limit):
    return poloniex.returnTradeHistory(currencyPair, start, end, limit)

# Returns the past 200 trades for a given market, or up to 50,000
# trades between a range specified in UNIX timestamps by the "start"
# and "end" GET parameters.

def getTradeHistoryPublic(poloniex, currencyPair, start, end):
    return poloniex.returnTradeHistory(currencyPair, start, end)