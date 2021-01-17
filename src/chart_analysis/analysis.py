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
        self.rsi_btc = ACTION.ERROR
        self.rsi_eth = ACTION.ERROR
        self.rsi_ltc = ACTION.ERROR

        self.stochastique_btc = ACTION.ERROR
        self.stochastique_eth = ACTION.ERROR
        self.stochastique_ltc = ACTION.ERROR

        self.cci_btc = ACTION.ERROR
        self.cci_eth = ACTION.ERROR
        self.cci_ltc = ACTION.ERROR

        self.adi_btc = ACTION.ERROR
        self.adi_eth = ACTION.ERROR
        self.adi_ltc = ACTION.ERROR

        self.awesome_btc = ACTION.ERROR
        self.awesome_eth = ACTION.ERROR
        self.awesome_ltc = ACTION.ERROR

        self.momentum_btc = ACTION.ERROR
        self.momentum_eth = ACTION.ERROR
        self.momentum_ltc = ACTION.ERROR

        self.macd_btc = ACTION.ERROR
        self.macd_eth = ACTION.ERROR
        self.macd_ltc = ACTION.ERROR

        self.stoch_rsi_btc = ACTION.ERROR
        self.stoch_rsi_eth = ACTION.ERROR
        self.stoch_rsi_ltc = ACTION.ERROR

        self.bull_bear_btc = ACTION.ERROR
        self.bull_bear_eth = ACTION.ERROR
        self.bull_bear_ltc = ACTION.ERROR

        self.sma_5_btc = ACTION.ERROR
        self.sma_5_eth = ACTION.ERROR
        self.sma_5_ltc = ACTION.ERROR

        self.ema_5_btc = ACTION.ERROR
        self.ema_5_eth = ACTION.ERROR
        self.ema_5_ltc = ACTION.ERROR

        self.sma_10_btc = ACTION.ERROR
        self.sma_10_eth = ACTION.ERROR
        self.sma_10_ltc = ACTION.ERROR

        self.ema_10_btc = ACTION.ERROR
        self.ema_10_eth = ACTION.ERROR
        self.ema_10_ltc = ACTION.ERROR

        self.sma_20_btc = ACTION.ERROR
        self.sma_20_eth = ACTION.ERROR
        self.sma_20_ltc = ACTION.ERROR

        self.ema_20_btc = ACTION.ERROR
        self.ema_20_eth = ACTION.ERROR
        self.ema_20_ltc = ACTION.ERROR

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
        self.status_reset("btc")

        self.rsi_btc = rsi("USDT_BTC")
        self.status_update("btc", self.rsi_btc)
        self.stochastique_btc = stochastique("USDT_BTC")
        self.status_update("btc", self.stochastique_btc)
        self.cci_btc = cci("USDT_BTC")
        self.status_update("btc", self.cci_btc)
        self.adi_btc = adi("USDT_BTC")
        self.status_update("btc", self.adi_btc)
        self.awesome_btc = awesome("USDT_BTC")
        self.status_update("btc", self.awesome_btc)
        self.momentum_btc = momentum("USDT_BTC")
        self.status_update("btc", self.momentum_btc)
        self.macd_btc = macd("USDT_BTC")
        self.status_update("btc", self.macd_btc)
        self.stoch_rsi_btc = stoch_rsi("USDT_BTC")
        self.status_update("btc", self.stoch_rsi_btc)
        self.bull_bear_btc = bull_bear("USDT_BTC")
        self.status_update("btc", self.bull_bear_btc)
        self.sma_5_btc = sma_5("USDT_BTC")
        self.status_update("btc", self.sma_5_btc)
        self.ema_5_btc = ema_5("USDT_BTC")
        self.status_update("btc", self.ema_5_btc)
        self.sma_10_btc = sma_10("USDT_BTC")
        self.status_update("btc", self.sma_10_btc)
        self.ema_10_btc = ema_10("USDT_BTC")
        self.status_update("btc", self.ema_10_btc)
        self.sma_20_btc = sma_20("USDT_BTC")
        self.status_update("btc", self.sma_20_btc)
        self.ema_20_btc = ema_20("USDT_BTC")
        self.status_update("btc", self.ema_20_btc)
    
    def eth_update(self):
        self.status_reset("eth")

        self.rsi_eth = rsi("USDT_ETH")
        self.status_update("eth", self.rsi_eth)
        self.stochastique_eth = stochastique("USDT_ETH")
        self.status_update("eth", self.stochastique_eth)
        self.cci_eth = cci("USDT_ETH")
        self.status_update("eth", self.cci_eth)
        self.adi_eth = adi("USDT_ETH")
        self.status_update("eth", self.adi_eth)
        self.awesome_eth = awesome("USDT_ETH")
        self.status_update("eth", self.awesome_eth)
        self.momentum_eth = momentum("USDT_ETH")
        self.status_update("eth", self.momentum_eth)
        self.macd_eth = macd("USDT_ETH")
        self.status_update("eth", self.macd_eth)
        self.stoch_rsi_eth = stoch_rsi("USDT_ETH")
        self.status_update("eth", self.stoch_rsi_eth)
        self.bull_bear_eth = bull_bear("USDT_ETH")
        self.status_update("eth", self.bull_bear_eth)
        self.sma_5_eth = sma_5("USDT_ETH")
        self.status_update("eth", self.sma_5_eth)
        self.ema_5_eth = ema_5("USDT_ETH")
        self.status_update("eth", self.ema_5_eth)
        self.sma_10_eth = sma_10("USDT_ETH")
        self.status_update("eth", self.sma_10_eth)
        self.ema_10_eth = ema_10("USDT_ETH")
        self.status_update("eth", self.ema_10_eth)
        self.sma_20_eth = sma_20("USDT_ETH")
        self.status_update("eth", self.sma_20_eth)
        self.ema_20_eth = ema_20("USDT_ETH")
        self.status_update("eth", self.ema_20_eth)

    def ltc_update(self):
        self.status_reset("ltc")

        self.rsi_ltc = rsi("USDT_LTC")
        self.status_update("ltc", self.rsi_ltc)
        self.stochastique_ltc = stochastique("USDT_LTC")
        self.status_update("ltc", self.stochastique_ltc)
        self.cci_ltc = cci("USDT_LTC")
        self.status_update("ltc", self.cci_ltc)
        self.adi_ltc = adi("USDT_LTC")
        self.status_update("ltc", self.adi_ltc)
        self.awesome_ltc = awesome("USDT_LTC")
        self.status_update("ltc", self.awesome_ltc)
        self.momentum_ltc = momentum("USDT_LTC")
        self.status_update("ltc", self.momentum_ltc)
        self.macd_ltc = macd("USDT_LTC")
        self.status_update("ltc", self.macd_ltc)
        self.stoch_rsi_ltc = stoch_rsi("USDT_LTC")
        self.status_update("ltc", self.stoch_rsi_ltc)
        self.bull_bear_ltc = bull_bear("USDT_LTC")
        self.status_update("ltc", self.bull_bear_ltc)
        self.sma_5_ltc = sma_5("USDT_LTC")
        self.status_update("ltc", self.sma_5_ltc)
        self.ema_5_ltc = ema_5("USDT_LTC")
        self.status_update("ltc", self.ema_5_ltc)
        self.sma_10_ltc = sma_10("USDT_LTC")
        self.status_update("ltc", self.sma_10_ltc)
        self.ema_10_ltc = ema_10("USDT_LTC")
        self.status_update("ltc", self.ema_10_ltc)
        self.sma_20_ltc = sma_20("USDT_LTC")
        self.status_update("ltc", self.sma_20_ltc)
        self.ema_20_ltc = ema_20("USDT_LTC")
        self.status_update("ltc", self.ema_20_ltc)
    
    def status_update(self, crypto, status):
        if status == ACTION.BUY and crypto == "btc":
            self.nbr_buy_btc += 1
        if status == ACTION.SELL and crypto == "btc":
            self.nbr_sell_btc += 1
        if status == ACTION.NEUTRAL and crypto == "btc":
            self.nbr_neutral_btc += 1

        if status == ACTION.BUY and crypto == "eth":
            self.nbr_buy_eth += 1
        if status == ACTION.SELL and crypto == "eth":
            self.nbr_sell_eth += 1
        if status == ACTION.NEUTRAL and crypto == "eth":
            self.nbr_neutral_eth += 1

        if status == ACTION.BUY and crypto == "ltc":
            self.nbr_buy_ltc += 1
        if status == ACTION.SELL and crypto == "ltc":
            self.nbr_sell_ltc += 1
        if status == ACTION.NEUTRAL and crypto == "ltc":
            self.nbr_neutral_ltc += 1
        return 0
    
    def status_reset(self, crypto):
        if crypto == "btc":
            self.nbr_buy_btc = 0
            self.nbr_neutral_btc = 0
            self.nbr_sell_btc = 0
        
        if crypto == "eth":     
            self.nbr_buy_eth = 0
            self.nbr_neutral_eth = 0
            self.nbr_sell_eth = 0
        
        if crypto == "ltc":  
            self.nbr_buy_ltc = 0
            self.nbr_neutral_ltc = 0
            self.nbr_sell_ltc = 0
    
    # finish all get

    def get_rsi(self, crypto):
        if crypto == "BTC":
            return self.rsi_btc
        if crypto == "ETH":     
            return self.rsi_eth
        if crypto == "LTC":  
            return self.rsi_ltc
    
    # dont forget the get for the green buy / red sell / white neutral

    def get_status(self, crypto):
        return 0

    # dont forget the get for the result, buy/ sell ?

    def get_result(self, crypto):
        return 0
    
    def get_status_string(self, crypto):
        if crypto == "BTC":
            status = str(self.nbr_buy_btc) + " Buy / " + str(self.nbr_sell_btc) + " Sell / " + str(self.nbr_neutral_btc) + " Neutral"
            return status
        if crypto == "ETH":
            status = str(self.nbr_buy_eth) + " Buy / " + str(self.nbr_sell_eth) + " Sell / " + str(self.nbr_neutral_eth) + " Neutral"
            return status
        if crypto == "LTC":
            status = str(self.nbr_buy_ltc) + " Buy / " + str(self.nbr_sell_ltc) + " Sell / " + str(self.nbr_neutral_ltc) + " Neutral"
            return status


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