#!/usr/bin/env python3

from enum import Enum
import sys
import string
import time
import math
from poloniex import Poloniex
import os

import chart_analysis.analysis #pylint: disable=import-error

import param #pylint: disable=import-error

# The Relative Strength Index (RSI9 or RSI14) is a well versed momentum based oscillator which is used to measure the speed (velocity)
# as well as the change (magnitude) of directional price movements. 

def sma_5(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 5):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 5

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("\nsma 5     " + str(sma))

    if sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.BUY
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.SELL
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def sma_10(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 10):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp

    sma = cp_sum / 10

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("sma 10    " + str(sma))

    if sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.BUY
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.SELL
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def sma_20(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0

    for i in range(0, 20):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp

    sma = cp_sum / 20

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("sma 20    " + str(sma))

    if sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.BUY
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.SELL
    if sma > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def ema_5(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0
    multiplier = (2 / (5 + 1))

    for i in range(1, 6):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 5

    ema = (float(param.charts_json.get_candle(json_data, "close")[candles-1]) - sma) * multiplier + sma

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("ema 5     " + str(ema))

    if ema < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.BUY
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.SELL
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.005:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def ema_10(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0
    multiplier = (2 / (11 + 1))

    for i in range(1, 11):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 10

    ema = (float(param.charts_json.get_candle(json_data, "close")[candles-1]) - sma) * multiplier + sma

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("ema 10    " + str(ema))

    if ema < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.BUY
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.SELL
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.01:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

def ema_20(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0
    multiplier = (2 / (20 + 1))

    for i in range(1, 21):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 20

    ema = (float(param.charts_json.get_candle(json_data, "close")[candles-1]) - sma) * multiplier + sma

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("ema 20    " + str(ema))

    if ema < float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.BUY
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.SELL
    if ema > float(param.charts_json.get_candle(json_data, "close")[candles-i]) - float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02 and sma < float(param.charts_json.get_candle(json_data, "close")[candles-i]) + float(param.charts_json.get_candle(json_data, "close")[candles-i])*0.02:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR