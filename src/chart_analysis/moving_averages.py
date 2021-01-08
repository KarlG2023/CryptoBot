#!/usr/bin/env python3

from enum import Enum
import sys
import string
import time
import math
from poloniex import Poloniex
import os

import chart_analysis.analysis #pylint: disable=import-error

import param_init #pylint: disable=import-error

# The Relative Strength Index (RSI9 or RSI14) is a well versed momentum based oscillator which is used to measure the speed (velocity)
# as well as the change (magnitude) of directional price movements. 

def sma_5(json_data):

    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 5):
        cp = float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 5

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("sma 5     " + str(sma))

    if sma < 30:
        return chart_analysis.analysis.ACTION.BUY
    if sma > 70:
        return chart_analysis.analysis.ACTION.SELL
    if sma > 30 and sma < 70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def sma_10(json_data):

    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 10):
        cp = float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp

    sma = cp_sum / 10

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("sma 10    " + str(sma))

    if sma < 30:
        return chart_analysis.analysis.ACTION.BUY
    if sma > 70:
        return chart_analysis.analysis.ACTION.SELL
    if sma > 30 and sma < 70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def sma_20(json_data):

    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 20):
        cp = float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp

    sma = cp_sum / 20

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("sma 20    " + str(sma))

    if sma < 30:
        return chart_analysis.analysis.ACTION.BUY
    if sma > 70:
        return chart_analysis.analysis.ACTION.SELL
    if sma > 30 and sma < 70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR
