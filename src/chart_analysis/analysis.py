#!/usr/bin/env python3

from enum import Enum
import sys
import string
import math
from poloniex import Poloniex
import os

import chart_analysis.oscillators #pylint: disable=import-error
import chart_analysis.moving_averages #pylint: disable=import-error

import data.charts #pylint: disable=import-error
import data.currencies #pylint: disable=import-error

import param_init #pylint: disable=import-error

class ACTION(Enum):
    BUY = 1
    NEUTRAL = 2
    SELL = 3
    ERROR = 4

# oscillators

def rsi(pair):
    return chart_analysis.oscillators.rsi_oscillator(param_init.charts_json.get_json_data(pair))

def stochastique(pair):
    return chart_analysis.oscillators.stochastique_oscillator(param_init.charts_json.get_json_data(pair))

def cci(pair):
    return chart_analysis.oscillators.cci_oscillator(param_init.charts_json.get_json_data(pair))

# moving_averages

def sma_5(pair):
    return chart_analysis.moving_averages.sma_5(param_init.charts_json.get_json_data(pair))

def sma_10(pair):
    return chart_analysis.moving_averages.sma_10(param_init.charts_json.get_json_data(pair))

def sma_20(pair):
    return chart_analysis.moving_averages.sma_20(param_init.charts_json.get_json_data(pair))