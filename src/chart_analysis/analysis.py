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

import param #pylint: disable=import-error

class ACTION(Enum):
    BUY = 1
    NEUTRAL = 2
    SELL = 3
    ERROR = 4

class analysis:
    def __init__(self):
        self.rsi_btc = rsi("USDT_BTC")
        self.rsi_eth = rsi("USDT_ETH")
        self.rsi_ltc = rsi("USDT_LTC")

        self.stochastique_btc = stochastique("USDT_BTC")
        self.stochastique_eth = stochastique("USDT_ETH")
        self.stochastique_ltc = stochastique("USDT_LTC")

        self.cci_btc = cci("USDT_BTC")
        self.cci_eth = cci("USDT_ETH")
        self.cci_ltc = cci("USDT_LTC")

        self.adi_btc = adi("USDT_BTC")
        self.adi_eth = adi("USDT_ETH")
        self.adi_ltc = adi("USDT_LTC")

        self.awesome_btc = awesome("USDT_BTC")
        self.awesome_eth = awesome("USDT_ETH")
        self.awesome_ltc = awesome("USDT_LTC")

        self.momentum_btc = momentum("USDT_BTC")
        self.momentum_eth = momentum("USDT_ETH")
        self.momentum_ltc = momentum("USDT_LTC")

        self.macd_btc = macd("USDT_BTC")
        self.macd_eth = macd("USDT_ETH")
        self.macd_ltc = macd("USDT_LTC")

        self.stoch_rsi_btc = stoch_rsi("USDT_BTC")
        self.stoch_rsi_eth = stoch_rsi("USDT_ETH")
        self.stoch_rsi_ltc = stoch_rsi("USDT_LTC")

        self.bull_bear_btc = bull_bear("USDT_BTC")
        self.bull_bear_eth = bull_bear("USDT_ETH")
        self.bull_bear_ltc = bull_bear("USDT_LTC")

        self.sma_5_btc = sma_5("USDT_BTC")
        self.sma_5_eth = sma_5("USDT_ETH")
        self.sma_5_ltc = sma_5("USDT_LTC")

        self.ema_5_btc = ema_5("USDT_BTC")
        self.ema_5_eth = ema_5("USDT_ETH")
        self.ema_5_ltc = ema_5("USDT_LTC")

        self.sma_10_btc = sma_10("USDT_BTC")
        self.sma_10_eth = sma_10("USDT_ETH")
        self.sma_10_ltc = sma_10("USDT_LTC")

        self.ema_10_btc = ema_10("USDT_BTC")
        self.ema_10_eth = ema_10("USDT_ETH")
        self.ema_10_ltc = ema_10("USDT_LTC")

        self.sma_20_btc = sma_20("USDT_BTC")
        self.sma_20_eth = sma_20("USDT_ETH")
        self.sma_20_ltc = sma_20("USDT_LTC")

        self.ema_20_btc = ema_20("USDT_BTC")
        self.ema_20_eth = ema_20("USDT_ETH")
        self.ema_20_ltc = ema_20("USDT_LTC")

        self.nbr_buy_btc = 0
        self.nbr_buy_eth = 0
        self.nbr_buy_ltc = 0
        
        self.nbr_neutral_btc = 0
        self.nbr_neutral_eth = 0
        self.nbr_neutral_ltc = 0
        
        self.nbr_sell_btc = 0
        self.nbr_sell_eth = 0
        self.nbr_sell_ltc = 0
    
    def btc_update(self):
        self.rsi_btc = rsi("USDT_BTC")
        self.stochastique_btc = stochastique("USDT_BTC")
        self.cci_btc = cci("USDT_BTC")
        self.adi_btc = adi("USDT_BTC")
        self.awesome_btc = awesome("USDT_BTC")
        self.momentum_btc = momentum("USDT_BTC")
        self.macd_btc = macd("USDT_BTC")
        self.stoch_rsi_btc = stoch_rsi("USDT_BTC")
        self.bull_bear_btc = bull_bear("USDT_BTC")
        self.sma_5_btc = sma_5("USDT_BTC")
        self.ema_5_btc = ema_5("USDT_BTC")
        self.sma_10_btc = sma_10("USDT_BTC")
        self.ema_10_btc = ema_10("USDT_BTC")
        self.sma_20_btc = sma_20("USDT_BTC")
        self.ema_20_btc = ema_20("USDT_BTC")
    
    def eth_update(self):
        self.rsi_eth = rsi("USDT_ETH")
        self.stochastique_eth = stochastique("USDT_ETH")
        self.cci_eth = cci("USDT_ETH")
        self.adi_eth = adi("USDT_ETH")
        self.awesome_eth = awesome("USDT_ETH")
        self.momentum_eth = momentum("USDT_ETH")
        self.macd_eth = macd("USDT_ETH")
        self.stoch_rsi_eth = stoch_rsi("USDT_ETH")
        self.bull_bear_eth = bull_bear("USDT_ETH")
        self.sma_5_eth = sma_5("USDT_ETH")
        self.ema_5_eth = ema_5("USDT_ETH")
        self.sma_10_eth = sma_10("USDT_ETH")
        self.ema_10_eth = ema_10("USDT_ETH")
        self.sma_20_eth = sma_20("USDT_ETH")
        self.ema_20_eth = ema_20("USDT_ETH")

    def ltc_update(self):
        self.rsi_ltc = rsi("USDT_LTC")
        self.stochastique_ltc = stochastique("USDT_LTC")
        self.cci_ltc = cci("USDT_LTC")
        self.adi_ltc = adi("USDT_LTC")
        self.awesome_ltc = awesome("USDT_LTC")
        self.momentum_ltc = momentum("USDT_LTC")
        self.macd_ltc = macd("USDT_LTC")
        self.stoch_rsi_ltc = stoch_rsi("USDT_LTC")
        self.bull_bear_ltc = bull_bear("USDT_LTC")
        self.sma_5_ltc = sma_5("USDT_LTC")
        self.ema_5_ltc = ema_5("USDT_LTC")
        self.sma_10_ltc = sma_10("USDT_LTC")
        self.ema_10_ltc = ema_10("USDT_LTC")
        self.sma_20_ltc = sma_20("USDT_LTC")
        self.ema_20_ltc = ema_20("USDT_LTC")
    
    def status_update(self):
        return 0
        

# oscillators

def rsi(pair):
    return chart_analysis.oscillators.rsi_oscillator(param.charts_json.get_json_data(pair))

def stochastique(pair):
    return chart_analysis.oscillators.stochastique_oscillator(param.charts_json.get_json_data(pair))

def cci(pair):
    return chart_analysis.oscillators.cci_oscillator(param.charts_json.get_json_data(pair))

def adi(pair):
    return chart_analysis.oscillators.adi_oscillator(param.charts_json.get_json_data(pair))

def awesome(pair):
    return chart_analysis.oscillators.AwesomeOscillator(param.charts_json.get_json_data(pair))

def momentum(pair):
    return chart_analysis.oscillators.momentum_oscillator(param.charts_json.get_json_data(pair))

def macd(pair):
    return chart_analysis.oscillators.macd_oscillator(param.charts_json.get_json_data(pair))

def stoch_rsi(pair):
    return chart_analysis.oscillators.stochastique_rsi(param.charts_json.get_json_data(pair))

def bull_bear(pair):
    return chart_analysis.oscillators.bull_bear_power(param.charts_json.get_json_data(pair))

# moving_averages

def sma_5(pair):
    return chart_analysis.moving_averages.sma_5(param.charts_json.get_json_data(pair))

def ema_5(pair):
    return chart_analysis.moving_averages.ema_5(param.charts_json.get_json_data(pair))

def sma_10(pair):
    return chart_analysis.moving_averages.sma_10(param.charts_json.get_json_data(pair))

def ema_10(pair):
    return chart_analysis.moving_averages.ema_10(param.charts_json.get_json_data(pair))

def sma_20(pair):
    return chart_analysis.moving_averages.sma_20(param.charts_json.get_json_data(pair))

def ema_20(pair):
    return chart_analysis.moving_averages.ema_20(param.charts_json.get_json_data(pair))