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

def rsi_oscillator(json_data):
    B = 0
    H = 0
    nb_B = 0
    nb_H = 0
    # print(json_data)
    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    for i in range(0, 13):
        if float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) > float(param_init.charts_json.get_candle(json_data, "close")[candles-i]):
            B += float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) - float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
            nb_B += 1
        else:
            H += float(param_init.charts_json.get_candle(json_data, "close")[candles-i]) - float(param_init.charts_json.get_candle(json_data, "open")[candles-i])
            nb_H += 1
    B = B / nb_B
    H = H / nb_H # open = high close = low ?
    rsi = 100 - (100 / (1 + (H / B)))

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print(str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "   " + str(rsi))

    if rsi < 30:
        return chart_analysis.analysis.ACTION.BUY
    if rsi > 70:
        return chart_analysis.analysis.ACTION.SELL
    if rsi > 30 and rsi < 70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# L’oscillateur stochastique (14) est un indicateur momentum qui compare le cours de clôture le plus récent au range précédent sur une période donnée.
# Contrairement à d’autres oscillateurs, il ne suit pas les cours ou le volume, mais la rapidité et le momentum du marché.

def stochastique_oscillator(json_data):
    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    current_close = float(param_init.charts_json.get_candle(json_data, "close")[candles])
    lowest_low = float(param_init.charts_json.get_candle(json_data, "low")[candles])
    highest_high = float(param_init.charts_json.get_candle(json_data, "high")[candles])

    for i in range(0, 13):
        if lowest_low > float(param_init.charts_json.get_candle(json_data, "low")[candles-i]):
            lowest_low = float(param_init.charts_json.get_candle(json_data, "low")[candles-i])
        if highest_high < float(param_init.charts_json.get_candle(json_data, "high")[candles-i]):
            highest_high = float(param_init.charts_json.get_candle(json_data, "high")[candles-i])

    # print(current_close)
    # print(lowest_low)
    # print(highest_high)

    stochastique = (100*(current_close - lowest_low)/(highest_high - lowest_low))

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("           " + str(stochastique))

    if stochastique < 20:
        return chart_analysis.analysis.ACTION.BUY
    if stochastique > 80:
        return chart_analysis.analysis.ACTION.SELL
    if stochastique > 20 and stochastique < 80:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# Assez proche de l'indicateur Stochastique, le Commodity Channel Index a un comportement particulièrement nerveux dans son
# évolution et peut être rebutant à la première lecture tant les oscillations sont courtes dans leur période.

# def cci_oscillator(json_data):
#     for the_last_14_days:
#         cours_m = (low + high + closure) / 3
#     for the_last_14_days:
#         cmm = 
#     # ...
#     # ...
    
#     if cci < -100:
#         return ACTION.BUY
#     if cci > 100:
#         return ACTION.SELL
#     if cci > -100 and cci < 100:
#         return ACTION.NEUTRAL
#     return ACTION.ERROR