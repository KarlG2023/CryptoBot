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

def rsi_oscillator(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    B = 0
    H = 0
    nb_B = 0
    nb_H = 0

    for i in range(0, 14):
        if float(param.charts_json.get_candle(json_data, "open")[candles-i]) > float(param.charts_json.get_candle(json_data, "close")[candles-i]):
            B -= float(param.charts_json.get_candle(json_data, "open")[candles-i]) / float(param.charts_json.get_candle(json_data, "close")[candles-i]) - 1
            nb_B += 1
        else:
            H += float(param.charts_json.get_candle(json_data, "close")[candles-i]) / float(param.charts_json.get_candle(json_data, "open")[candles-i]) - 1
            nb_H += 1
    B = B / 14
    H = H / 14
    rsi = 100 - (100 / (1 + (H / -B)))

#    if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
#        print(str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S")) + "\n")
#        print("rsi_14    " + str(rsi))

    if rsi < 35:
        return chart_analysis.analysis.ACTION.BUY
    if rsi > 60:
        return chart_analysis.analysis.ACTION.SELL
    if rsi > 35 and rsi < 60:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# L’oscillateur stochastique (14) est un indicateur momentum qui compare le cours de clôture le plus récent au range précédent sur une période donnée.
# Contrairement à d’autres oscillateurs, il ne suit pas les cours ou le volume, mais la rapidité et le momentum du marché.

def stochastique_oscillator(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    current_close = float(param.charts_json.get_candle(json_data, "close")[candles])
    lowest_low = float(param.charts_json.get_candle(json_data, "low")[candles])
    highest_high = float(param.charts_json.get_candle(json_data, "high")[candles])

    for i in range(0, 13):
        if lowest_low > float(param.charts_json.get_candle(json_data, "low")[candles-i]):
            lowest_low = float(param.charts_json.get_candle(json_data, "low")[candles-i])
        if highest_high < float(param.charts_json.get_candle(json_data, "high")[candles-i]):
            highest_high = float(param.charts_json.get_candle(json_data, "high")[candles-i])

    stochastique = (100*(current_close - lowest_low)/(highest_high - lowest_low))

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("stocha    " + str(stochastique))

    if stochastique < 30:
        return chart_analysis.analysis.ACTION.BUY
    if stochastique > 70:
        return chart_analysis.analysis.ACTION.SELL
    if stochastique > 30 and stochastique < 70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# Assez proche de l'indicateur Stochastique, le Commodity Channel Index a un comportement particulièrement nerveux dans son
# évolution et peut être rebutant à la première lecture tant les oscillations sont courtes dans leur période.

def cci_oscillator(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    tp = 0
    current_tp = 0
    standart_deviation = 0

    for i in range(0, 19):
        tl = float(param.charts_json.get_candle(json_data, "low")[candles-i])
        th = float(param.charts_json.get_candle(json_data, "high")[candles-i])
        tc = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        tp = tp + ((tl + th + tc) / 3)
        if (i == 0):
            current_tp = tp

    sma = tp / 19

    for i in range(0, 19):
        tl =  float(param.charts_json.get_candle(json_data, "low")[candles-i])
        th =  float(param.charts_json.get_candle(json_data, "high")[candles-i])
        tc = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        tp = (tl + th + tc) / 3
        standart_deviation = standart_deviation + abs(sma - tp)

    standart_deviation = standart_deviation / 19
    cci = (current_tp - sma) / (0.015 * standart_deviation)
    
    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("cci_20    " + str(cci))
    
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
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    stocha = stochastique_oscillator(json_data)
    positiv_dm = 0.00
    negativ_dm = 0.00
    tr = 0
    POSITIV_DM14 = [0.00 for x in range(14)]
    NEGATIV_DM14 = [0.00 for x in range(14)]
    TR14 = [0.00 for x in range(14)]
    DX = [0.00 for x in range(14)]
    adi = 0

    for i in range(0, 28):
        cur_high_mclose = float(param.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param.charts_json.get_candle(json_data, "close")[candles+i-28])
        cur_high_mpclose = abs(float(param.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param.charts_json.get_candle(json_data, "close")[candles+i+1-28]))
        cur_low_mpclose = abs(float(param.charts_json.get_candle(json_data, "low")[candles+i-28]) - float(param.charts_json.get_candle(json_data, "close")[candles+i+1-28]))

        # tr on 14 days
        if cur_high_mclose > max(cur_high_mpclose, cur_low_mpclose):
            TR14[i%14] = cur_high_mclose
        if cur_high_mpclose > max(cur_high_mclose, cur_low_mpclose):
            TR14[i%14] =  cur_high_mpclose
        if cur_low_mpclose > max(cur_high_mclose, cur_high_mpclose):
            TR14[i%14] =  cur_low_mpclose

        chmph = float(param.charts_json.get_candle(json_data, "high")[candles+i-28]) - float(param.charts_json.get_candle(json_data, "high")[candles+i-1-28])
        plmcl = float(param.charts_json.get_candle(json_data, "low")[candles+i-1-28]) - float(param.charts_json.get_candle(json_data, "low")[candles+i-28])
        
        # positiv dm and negativ dm on 14 days
        if (chmph > plmcl):
            POSITIV_DM14[i%14] = chmph
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
    adi /= 14

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("adi       " + str(adi))
    
    if adi < 20 and stocha == chart_analysis.analysis.ACTION.BUY:
        return chart_analysis.analysis.ACTION.BUY
    if adi < 20 and stocha == chart_analysis.analysis.ACTION.SELL:
        return chart_analysis.analysis.ACTION.SELL
    if adi < 20 and stocha == chart_analysis.analysis.ACTION.NEUTRAL:
        return chart_analysis.analysis.ACTION.NEUTRAL

    if adi > 30 and stocha == chart_analysis.analysis.ACTION.BUY:
        return chart_analysis.analysis.ACTION.BUY
    if adi > 30 and stocha == chart_analysis.analysis.ACTION.SELL:
        return chart_analysis.analysis.ACTION.SELL
    if adi > 30 and stocha == chart_analysis.analysis.ACTION.NEUTRAL:
        return chart_analysis.analysis.ACTION.NEUTRAL
    
    if adi > 20 and adi < 30:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# The Awesome Oscillator is an indicator used to measure market momentum.
# AO calculates the difference of a 34 Period and 5 Period Simple Moving Averages.

def AwesomeOscillatorSMA(json_data, nb):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0
    for i in range(0, nb):
        cp = (float(param.charts_json.get_candle(json_data, "high")[candles-i]) + float(param.charts_json.get_candle(json_data, "low")[candles-i])) / 2
        cp_sum = cp_sum + cp    
    sma = cp_sum / nb
    return sma

def AwesomeOscillator(json_data):
    AO = AwesomeOscillatorSMA(json_data, 5) - AwesomeOscillatorSMA(json_data, 34)

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("AO        " + str(AO))

    if AO > 10:
        return chart_analysis.analysis.ACTION.SELL
    if AO < 10:
        return chart_analysis.analysis.ACTION.BUY
    return chart_analysis.analysis.ACTION.ERROR

# The Momentum Indicator (MOM) is a leading indicator measuring a security's rate-of-change.
# It compares the current price with the previous price from a number of periods ago.

def momentum_oscillator(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1

    momentum = 100 * (float(param.charts_json.get_candle(json_data, "close")[candles]) / float(param.charts_json.get_candle(json_data, "close")[candles-10]))

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("MOMENTUM  " + str(momentum))

    if momentum < 80:
        return chart_analysis.analysis.ACTION.BUY
    if momentum > 90:
        return chart_analysis.analysis.ACTION.SELL
    if momentum > 80 and momentum < 90:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# MACD is an extremely popular indicator used in technical analysis.
# MACD can be used to identify aspects of a security's overall trend.

def macd_ema(json_data, nb, from_nbr):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    multiplier = (2 / (nb + 1))
    cp_sum = 0
    for i in range(0, nb):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i-from_nbr])
        cp_sum = cp_sum + cp 
    sma = cp_sum / nb
    ema = (float(param.charts_json.get_candle(json_data, "close")[candles-1]) - sma) * multiplier + sma
    return ema

def macd_oscillator(json_data):
    MACD_LINE_EMA = [0.00 for x in range(9)]

    for i in range(0, 9):
        MACD_LINE_EMA[i] = macd_ema(json_data, 12, i) - macd_ema(json_data, 26, i)

    multiplier = (2 / (9 + 1))
    cp_sum = 0
    for i in range(0, 9):
        cp = MACD_LINE_EMA[i]
        cp_sum = cp_sum + cp    
    sma = cp_sum / 9

    signal_line = (MACD_LINE_EMA[0] - sma) * multiplier + sma

    macd_histogram = MACD_LINE_EMA[0] - signal_line

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("MACD      " + str(macd_histogram))

    if macd_histogram < 0:
        return chart_analysis.analysis.ACTION.SELL
    if macd_histogram > 0:
        return chart_analysis.analysis.ACTION.BUY
    return chart_analysis.analysis.ACTION.ERROR

# The Stochastic RSI indicator (Stoch RSI) is essentially an indicator of an indicator.
# It is used in technical analysis to provide a stochastic calculation to the RSI indicator. 

def rsi_past(json_data, nbr):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    B = 0
    H = 0
    nb_B = 0
    nb_H = 0

    for i in range(0, 14):
        if float(param.charts_json.get_candle(json_data, "open")[candles-i-nbr]) > float(param.charts_json.get_candle(json_data, "close")[candles-i-nbr]):
            B -= float(param.charts_json.get_candle(json_data, "open")[candles-i-nbr]) / float(param.charts_json.get_candle(json_data, "close")[candles-i-nbr]) - 1
            nb_B += 1
        else:
            H += float(param.charts_json.get_candle(json_data, "close")[candles-i-nbr]) / float(param.charts_json.get_candle(json_data, "open")[candles-i-nbr]) - 1
            nb_H += 1
    B = B / 14
    H = H / 14
    rsi = 100 - (100 / (1 + (H / -B)))
    return rsi

def stochastique_rsi(json_data):
    stoch_rsi = [0.00 for x in range(14)]
    low_rsi = 100
    high_rsi = 0

    for i in range(0, 14):
        stoch_rsi[i] = rsi_past(json_data, i)
        if low_rsi > stoch_rsi[i]:
            low_rsi = stoch_rsi[i]
        if high_rsi < stoch_rsi[i]:
            high_rsi = stoch_rsi[i]
    
    stoch_rsi = (rsi_past(json_data, 0) - low_rsi) / (high_rsi - low_rsi)

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("stochrsi  " + str(stoch_rsi))

    if stoch_rsi < 0.30:
        return chart_analysis.analysis.ACTION.BUY
    if stoch_rsi > 0.70:
        return chart_analysis.analysis.ACTION.SELL
    if stoch_rsi > 0.30 and stoch_rsi < 0.70:
        return chart_analysis.analysis.ACTION.NEUTRAL
    return chart_analysis.analysis.ACTION.ERROR

# The Bears Power oscillator was developed by Alexander Elder.
# It measures the difference between the lowest price and a 13-day Exponential Moving Average (EMA), plotted as a histogram. 

def ema_13(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1
    cp_sum = 0
    multiplier = (2 / (20 + 1))

    for i in range(1, 21):
        cp = float(param.charts_json.get_candle(json_data, "close")[candles-i])
        cp_sum = cp_sum + cp
    sma = cp_sum / 20

    ema = (float(param.charts_json.get_candle(json_data, "close")[candles-1]) - sma) * multiplier + sma

    return ema

def bull_bear_power(json_data):
    candles = len(param.charts_json.get_candle(json_data, "volume"))-1

    bull_bear = float(param.charts_json.get_candle(json_data, "low")[candles]) - ema_13(json_data)

    # if int(time.strftime("%M")) % 1 == 0 and int(time.strftime("%S")) == 0:
    #     print("bullbear  " + str(bull_bear))

    if bull_bear < 0:
        return chart_analysis.analysis.ACTION.BUY
    if bull_bear > 0:
        return chart_analysis.analysis.ACTION.SELL
    return chart_analysis.analysis.ACTION.ERROR