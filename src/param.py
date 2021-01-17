#!/usr/bin/env python3

import chart_analysis.analysis
import data.charts
import widgets.login

def init():
    global poloniex_obj
    poloniex_obj = widgets.login.log_UI()

def init_json():
    global charts_json, candle_size
    candle_size = 900
    charts_json = data.charts.charts_json(poloniex_obj, candle_size)
    cryptobot = chart_analysis.analysis.analysis()