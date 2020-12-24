#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

class ACTION(Enum):
    BUY = 1
    NEUTRAL = 2
    SELL = 3
    ERROR = 4

# The Relative Strength Index (RSI9 or RSI14) is a well versed momentum based oscillator which is used to measure the speed (velocity)
# as well as the change (magnitude) of directional price movements. 

def rsi_oscillator(json_data):
    B = descending_average
    H = ascending_average
    rsi = 100 - (100 / 1 + (H / B))
    if rsi < 30:
        return ACTION.BUY
    if rsi > 70:
        return ACTION.SELL
    if rsi > 30 and rsi < 70:
        return ACTION.NEUTRAL
    return ACTION.ERROR

# L’oscillateur stochastique (14) est un indicateur momentum qui compare le cours de clôture le plus récent au range précédent sur une période donnée.
# Contrairement à d’autres oscillateurs, il ne suit pas les cours ou le volume, mais la rapidité et le momentum du marché.

def stochastique_oscillator(json_data):
    stochastique = ((actual_val - min)/(max - min) * 100)
    if stochastique < 20:
        return ACTION.BUY
    if stochastique > 80:
        return ACTION.SELL
    if stochastique > 20 and stochastique < 80:
        return ACTION.NEUTRAL
    return ACTION.ERROR

# Assez proche de l'indicateur Stochastique, le Commodity Channel Index a un comportement particulièrement nerveux dans son
# évolution et peut être rebutant à la première lecture tant les oscillations sont courtes dans leur période.

def cci_oscillator(json_data):
    for the_last_14_days:
        cours_m = (low + high + closure) / 3
    for the_last_14_days:
        cmm = 
    # ...
    # ...
    
    if cci < -100:
        return ACTION.BUY
    if cci > 100:
        return ACTION.SELL
    if cci > -100 and cci < 100:
        return ACTION.NEUTRAL
    return ACTION.ERROR