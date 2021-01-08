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
    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    B = 0
    H = 0
    nb_B = 0
    nb_H = 0

    for i in range(0, 14):
        if float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) > float(param_init.charts_json.get_candle(json_data, "close")[candles-i]):
            B += float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) - float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
            nb_B += 1
        else:
            H += float(param_init.charts_json.get_candle(json_data, "close")[candles-i]) - float(param_init.charts_json.get_candle(json_data, "open")[candles-i])
            nb_H += 1
    B = B / nb_B
    H = H / nb_H
    print(B)
    print(H)
    rsi = 100 - (100 / (1 + (H / B)))

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print(str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "\n")
        print("rsi_14    " + str(rsi))

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

    stochastique = (100*(current_close - lowest_low)/(highest_high - lowest_low))

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("stocha    " + str(stochastique))

    if stochastique < 20:
        return chart_analysis.analysis.ACTION.BUY
    if stochastique > 80:
        return chart_analysis.analysis.ACTION.SELL
    if stochastique > 20 and stochastique < 80:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# Assez proche de l'indicateur Stochastique, le Commodity Channel Index a un comportement particulièrement nerveux dans son
# évolution et peut être rebutant à la première lecture tant les oscillations sont courtes dans leur période.

def cci_oscillator(json_data):
    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    tp = 0
    current_tp = 0
    standart_deviation = 0

    for i in range(0, 19):
        tl = float(param_init.charts_json.get_candle(json_data, "low")[candles-i])
        th = float(param_init.charts_json.get_candle(json_data, "high")[candles-i])
        tc = float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
        tp = tp + ((tl + th + tc) / 3)
        if (i == 0):
            current_tp = tp

    sma = tp / 19

    for i in range(0, 19):
        tl =  float(param_init.charts_json.get_candle(json_data, "low")[candles-i])
        th =  float(param_init.charts_json.get_candle(json_data, "high")[candles-i])
        tc = float(param_init.charts_json.get_candle(json_data, "close")[candles-i])
        tp = (tl + th + tc) / 3
        standart_deviation = standart_deviation + abs(sma - tp)

    standart_deviation = standart_deviation / 19
    cci = (current_tp - sma) / (0.015 * standart_deviation)
    
    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("cci_20    " + str(cci))
    
    if cci < -100:
        return chart_analysis.analysis.ACTION.BUY
    if cci > 100:
        return chart_analysis.analysis.ACTION.SELL
    if cci > -100 and cci < 100:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# ADX stands for Average Directional Movement Index and can be used to help measure the overall strength of a trend. 
# The ADX indicator is an average of expanding price range values.

# def average_directional_index(json_data):
#     candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
#     positiv_dm = 0.00
#     negativ_dm = 0.00
#     atr = 0

#     for i in range(0, 14):
#         positiv_dm = float(param_init.charts_json.get_candle(json_data, "high")[candles-i]) - float(param_init.charts_json.get_candle(json_data, "high")[candles-i-1])
#         negativ_dm = float(param_init.charts_json.get_candle(json_data, "low")[candles-i-1]) - float(param_init.charts_json.get_candle(json_data, "low")[candles-i])
#         tr = tr + abs(float(param_init.charts_json.get_candle(json_data, "high")[candles-i-1]) - float(param_init.charts_json.get_candle(json_data, "low")[candles-i-1]))

#     atr = tr / 14


#     adi = 0

#     if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
#         print("           " + str(adi))
    
#     if adi < 20:
#         return chart_analysis.analysis.ACTION.BUY
#     if adi > 25:
#         return chart_analysis.analysis.ACTION.SELL
#     if adi > 20 and adi < 25:
#         return chart_analysis.analysis.ACTION.NEUTRAL
#     return chart_analysis.analysis.ACTION.ERROR