#!/usr/bin/env python3

from enum import Enum
import sys
import string
import math
from poloniex import Poloniex
import os

import chart_analysis.oscillators #pylint: disable=import-error

import data.charts #pylint: disable=import-error
import data.currencies #pylint: disable=import-error

import param_init #pylint: disable=import-error

class ACTION(Enum):
    BUY = 1
    NEUTRAL = 2
    SELL = 3
    ERROR = 4


def rsi(pair):
    return chart_analysis.oscillators.rsi_oscillator(param_init.charts_json.get_json_data(pair))

def stochastique(pair):
    return chart_analysis.oscillators.stochastique_oscillator(param_init.charts_json.get_json_data(pair))