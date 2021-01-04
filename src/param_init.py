#!/usr/bin/env python3

import data.charts
import widgets.login

def init():
    global poloniex_obj 
    poloniex_obj = widgets.login.log_UI()

def init_json():
    global charts_json
    charts_json = data.charts.charts_json(poloniex_obj)