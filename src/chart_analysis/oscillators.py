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
            B -= float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) / float(param_init.charts_json.get_candle(json_data, "close")[candles-i]) - 1
            nb_B += 1
        else:
            H += float(param_init.charts_json.get_candle(json_data, "close")[candles-i]) / float(param_init.charts_json.get_candle(json_data, "open")[candles-i]) - 1
            nb_H += 1
    B = B / 14
    H = H / 14
    rsi = 100 - (100 / (1 + (H / -B)))

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

def adi_oscillator(json_data):
    candles = len(param_init.charts_json.get_candle(json_data, "volume"))-1
    positiv_dm = 0.00
    negativ_dm = 0.00
    tr = 0
    POSITIV_DM14 = [0.00 for x in range(14)]
    NEGATIV_DM14 = [0.00 for x in range(14)]
    TR14 = [0.00 for x in range(14)]
    DX = [0.00 for x in range(14)]
    adi = 0

    # first step need to start at 27th value and uses 14 values
    # smooth values by stocking previous adi on 5 values

    for i in range(0, 28):
        cur_high_mclose = float(param_init.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param_init.charts_json.get_candle(json_data, "close")[candles+i-28])
        cur_high_mpclose = abs(float(param_init.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param_init.charts_json.get_candle(json_data, "close")[candles+i+1-28]))
        cur_low_mpclose = abs(float(param_init.charts_json.get_candle(json_data, "low")[candles+i-28]) - float(param_init.charts_json.get_candle(json_data, "close")[candles+i+1-28]))

        # tr on 14 days
        if cur_high_mclose > max(cur_high_mpclose, cur_low_mpclose):
            TR14[i%14] = cur_high_mclose
        if cur_high_mpclose > max(cur_high_mclose, cur_low_mpclose):
            TR14[i%14] =  cur_high_mpclose
        if cur_low_mpclose > max(cur_high_mclose, cur_high_mpclose):
            TR14[i%14] =  cur_low_mpclose

        chmph = float(param_init.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param_init.charts_json.get_candle(json_data, "high")[candles+i-1-28])
        plmcl = float(param_init.charts_json.get_candle(json_data, "low")[candles+i-1-28]) - float(param_init.charts_json.get_candle(json_data, "low")[candles+i-28])
        
        # positiv dm and negativ dm on 14 days
        if (chmph > plmcl):
            POSITIV_DM14[i%14] = chmph
            # print(chmph)
        if (plmcl > chmph):
            NEGATIV_DM14[i%14] = plmcl
        
        if i > 14:
            for a in range(0, len(TR14)):
                tr += TR14[a]
    
            for b in range(0, len(POSITIV_DM14)):
                positiv_dm += POSITIV_DM14[b]
        
            for c in range(0, len(NEGATIV_DM14)):
                negativ_dm += NEGATIV_DM14[c]
            
            pdi = (positiv_dm / tr)*100
            ndi = (negativ_dm / tr)*100

            DX[i%14] = abs(pdi - ndi) / (pdi + ndi) * 100

            tr = 0
            positiv_dm = 0
            negativ_dm = 0

    for d in range(1, len(DX)):
        adi += DX[d]
        print(DX[d])
    adi /= 14
    print(adi)
    print("\n\n\n")

    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
        print("adi       " + str(adi))
    
    if adi < 20:
        return chart_analysis.analysis.ACTION.BUY
    if adi > 25:
        return chart_analysis.analysis.ACTION.SELL
    if adi > 20 and adi < 25:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR