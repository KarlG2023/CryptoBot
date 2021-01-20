#!/usr/bin/env python3

import time

import api_request.account #pylint: disable=import-error
import api_request.charts #pylint: disable=import-error
import api_request.trades #pylint: disable=import-error

import chart_analysis.analysis
import data.charts
import widgets.login

def init():
    global poloniex_obj, bot_status, server_status, window_x, window_y
    poloniex_obj = widgets.login.log_UI()
    bot_status = 0
    server_status = 1
    window_x = 1280
    window_y = 720


def init_account():
    global balance, trades_btc, trades_eth, trades_ltc

    # balance = api_request.account.get_balance(poloniex_obj)
    balance = {'USDT': 1000.0, 'BTC': 0.0, 'ETH': 0.0, 'LTC': 0.0} # test


    trades_btc = str(api_request.trades.getTradeHistory(poloniex_obj, "USDT_BTC", start=int(time.time())-(86400*30), end=int(time.time()), limit=10))
    trades_eth = str(api_request.trades.getTradeHistory(poloniex_obj, "USDT_ETH", start=int(time.time())-(86400*30), end=int(time.time()), limit=10))
    trades_ltc = str(api_request.trades.getTradeHistory(poloniex_obj, "USDT_ETH", start=int(time.time())-(86400*30), end=int(time.time()), limit=10))

def init_json():
    global candle_size, charts_json, cryptobot
    candle_size = 900
    charts_json = data.charts.charts_json(poloniex_obj, candle_size)
    cryptobot = chart_analysis.analysis.analysis()