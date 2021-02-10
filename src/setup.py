import sys
import poloniex
import PySide2
from cx_Freeze import setup, Executable

import api_request.account
import api_request.charts
import api_request.trades

import chart_analysis.analysis
import chart_analysis.moving_averages
import chart_analysis.oscillators

import data.charts
import data.currencies

import widgets.cryptos
import widgets.dashboard
import widgets.login
import widgets.parameters

import param

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "CryptoBot",
        version = "0.1",
        description = "A great trading app",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", icon="../assets/icon.ico", target_name="CryptoBot")])

# python3 setup.py build && cp -r ../assets build