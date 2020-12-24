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

# The Relative Strength Index (RSI) is a well versed momentum based oscillator which is used to measure the speed (velocity)
# as well as the change (magnitude) of directional price movements. 

def rsi(json_data):
    B = Moyenne des baisses
    H = moyenne des hausses
    rsi = 100 - (100 / 1 + (H / B))
    if rsi < 30:
        return ACTION.BUY
    if rsi > 70:
        return ACTION.SELL
    if rsi > 30 and rsi < 70:
        return ACTION.NEUTRAL
    return ACTION.ERROR