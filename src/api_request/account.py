#!/usr/bin/env python3

import sys
import string
import math
from poloniex import Poloniex
import os

def log(api_key, api_secret):
    try:
        polo = Poloniex(api_key, api_secret)
        return polo
    except Exception as e:
        print("Unexpected error:", e)
        exit(84)

# Returns all of your available balances.

def get_balance(poloniex):
    try:
        return poloniex.returnBalances()
    except:
        return {'1CR': 0.0, 'ABY': 0.0, 'AC': 0.0, 'ACH': 0.0, 'ADN': 0.0, 'AEON': 0.0, 'AERO': 0.0, 'AIR': 0.0, 'APH': 0.0, 'AUR': 0.0, 'AXIS': 0.0, 'BALLS': 0.0, 'BANK': 0.0, 'BBL': 0.0, 'BBR': 0.0, 'BCC': 0.0, 'BCN': 0.0, 'BDC': 0.0, 'BDG': 0.0, 'BELA': 0.0, 'BITS': 0.0, 'BLK': 0.0, 'BLOCK': 0.0, 'BLU': 0.0, 'BNS': 0.0, 'BONES': 0.0, 'BOST': 0.0, 'BTC': 0.0, 'BTCD': 0.0, 'BTCS': 0.0, 'BTM': 0.0, 'BTS': 0.0, 'BURN': 0.0, 'BURST': 0.0, 'C2': 0.0, 'CACH': 0.0, 'CAI': 0.0, 'CC': 0.0, 'CCN': 0.0, 'CGA': 0.0, 'CHA': 0.0, 'CINNI': 0.0, 'CLAM': 0.0, 'CNL': 0.0, 'CNMT': 0.0, 'CNOTE': 0.0, 'COMM': 0.0, 'CON': 0.0, 'CORG': 0.0, 'CRYPT': 0.0, 'CURE': 0.0, 'CYC': 0.0, 'DGB': 0.0, 'DICE': 0.0, 'DIEM': 0.0, 'DIME': 0.0, 'DIS': 0.0, 'DNS': 0.0, 'DOGE': 0.0, 'DASH': 0.0, 'DRKC': 0.0, 'DRM': 0.0, 'DSH': 0.0, 'DVK': 0.0, 'EAC': 0.0, 'EBT': 0.0, 'ECC': 0.0, 'EFL': 0.0, 'EMC2': 0.0, 'EMO': 0.0, 'ENC': 0.0, 'eTOK': 0.0, 'EXE': 0.0, 'FAC': 0.0, 'FCN': 0.0, 'FIBRE': 0.0, 'FLAP': 0.0, 'FLDC': 0.0, 'FLT': 0.0, 'FOX': 0.0, 'FRAC': 0.0, 'FRK': 0.0, 'FRQ': 0.0, 'FVZ': 0.0, 'FZ': 0.0, 'FZN': 0.0, 'GAP': 0.0, 'GDN': 0.0, 'GEMZ': 0.0, 'GEO': 0.0, 'GIAR': 0.0, 'GLB': 0.0, 'GAME': 0.0, 'GML': 0.0, 'GNS': 0.0, 'GOLD': 0.0, 'GPC': 0.0, 'GPUC': 0.0, 'GRCX': 0.0, 'GRS': 0.0, 'GUE': 0.0, 'H2O': 0.0, 'HIRO': 0.0, 'HOT': 0.0, 'HUC': 0.0, 'HVC': 0.0, 'HYP': 0.0, 'HZ': 0.0, 'IFC': 0.0, 'ITC': 0.0, 'IXC': 0.0, 'JLH': 0.0, 'JPC': 0.0, 'JUG': 0.0, 'KDC': 0.0, 'KEY': 0.0, 'LC': 0.0, 'LCL': 0.0, 'LEAF': 0.0, 'LGC': 0.0, 'LOL': 0.0, 'LOVE': 0.0, 'LQD': 0.0, 'LTBC': 0.0, 'LTC': 0.0, 'LTCX': 0.0, 'MAID': 0.0, 'MAST': 0.0, 'MAX': 0.0, 'MCN': 0.0, 'MEC': 0.0, 'METH': 0.0, 'MIL': 0.0, 'MIN': 0.0, 'MINT': 0.0, 'MMC': 0.0, 'MMNXT': 0.0, 'MMXIV': 0.0, 'MNTA': 0.0, 'MON': 0.0, 'MRC': 0.0, 'MRS': 0.0, 'OMNI': 0.0, 'MTS': 0.0, 'MUN': 0.0, 'MYR': 0.0, 'MZC': 0.0, 'N5X': 0.0, 'NAS': 0.0, 'NAUT': 0.0, 'NAV': 0.0, 'NBT': 0.0, 'NEOS': 0.0, 'NL': 0.0, 'NMC': 0.0, 'NOBL': 0.0, 'NOTE': 0.0, 'NOXT': 0.0, 'NRS': 0.0, 'NSR': 0.0, 'NTX': 0.0, 'NXT': 0.0, 'NXTI': 0.0, 'OPAL': 0.0, 'PAND': 0.0, 'PAWN': 0.0, 'PIGGY': 0.0, 'PINK': 0.0, 'PLX': 0.0, 'PMC': 0.0, 'POT': 0.0, 'PPC': 0.0, 'PRC': 0.0, 'PRT': 0.0, 'PTS': 0.0, 'Q2C': 0.0, 'QBK': 0.0, 'QCN': 0.0, 'QORA': 0.0, 'QTL': 0.0, 'RBY': 0.0, 'RDD': 0.0, 'RIC': 0.0, 'RZR': 0.0, 'SDC': 0.0, 'SHIBE': 0.0, 'SHOPX': 0.0, 'SILK': 0.0, 'SJCX': 0.0, 'SLR': 0.0, 'SMC': 0.0, 'SOC': 0.0, 'SPA': 0.0, 'SQL': 0.0, 'SRCC': 0.0, 'SRG': 0.0, 'SSD': 0.0, 'STR': 0.0, 'SUM': 0.0, 'SUN': 0.0, 'SWARM': 0.0, 'SXC': 0.0, 'SYNC': 0.0, 'SYS': 0.0, 'TAC': 0.0, 'TOR': 0.0, 'TRUST': 0.0, 'TWE': 0.0, 'UIS': 0.0, 'ULTC': 0.0, 'UNITY': 0.0, 'URO': 0.0, 'USDE': 0.0, 'USDT': 0.0, 'UTC': 0.0, 'UTIL': 0.0, 'UVC': 0.0, 'VIA': 0.0, 'VOOT': 0.0, 'VRC': 0.0, 'VTC': 0.0, 'WC': 0.0, 'WDC': 0.0, 'WIKI': 0.0, 'WOLF': 0.0, 'X13': 0.0, 'XAI': 0.0, 'XAP': 0.0, 'XBC': 0.0, 'XC': 0.0, 'XCH': 0.0, 'XCN': 0.0, 'XCP': 0.0, 'XCR': 0.0, 'XDN': 0.0, 'XDP': 0.0, 'XHC': 0.0, 'XLB': 0.0, 'XMG': 0.0, 'XMR': 0.0, 'XPB': 0.0, 'XPM': 0.0, 'XRP': 0.0, 'XSI': 0.0, 'XST': 0.0, 'XSV': 0.0, 'XUSD': 0.0, 'XXC': 0.0, 'YACC': 0.0, 'YANG': 0.0, 'YC': 0.0, 'YIN': 0.0, 'XVC': 0.0, 'FLO': 0.0, 'XEM': 0.0, 'ARCH': 0.0, 'HUGE': 0.0, 'GRC': 0.0, 'IOC': 0.0, 'INDEX': 0.0, 'ETH': 0.0, 'SC': 0.0, 'BCY': 0.0, 'EXP': 0.0, 'FCT': 0.0, 'BITUSD': 0.0, 'BITCNY': 0.0, 'RADS': 0.0, 'AMP': 0.0, 'VOX': 0.0, 'DCR': 0.0, 'LSK': 0.0, 'DAO': 0.0, 'LBC': 0.0, 'STEEM': 0.0, 'SBD': 0.0, 'ETC': 0.0, 'ARDR': 0.0, 'ZEC': 0.0, 'STRAT': 0.0, 'NXC': 0.0, 'PASC': 0.0, 'GNT': 0.0, 'GNO': 0.0, 'BCH': 0.0, 'ZRX': 0.0, 'CVC': 0.0, 'OMG': 0.0, 'GAS': 0.0, 'STORJ': 0.0, 'EOS': 0.0, 'USDC': 0.0, 'SNT': 0.0, 'KNC': 0.0, 'BAT': 0.0, 'LOOM': 0.0, 'QTUM': 0.0, 'BNT': 0.0, 'MANA': 0.0, 'FOAM': 0.0, 'BCHABC': 0.0, 'BCHSV': 0.0, 'NMR': 0.0, 'POLY': 0.0, 'LPT': 0.0, 'ATOM': 0.0, 'GRIN': 0.0, 'TRX': 0.0, 'ETHBNT': 0.0, 'BTT': 0.0, 'WIN': 0.0, 'BEAR': 0.0, 'BULL': 0.0, 'BUSD': 0.0, 'DAI': 0.0, 'LINK': 0.0, 'MKR': 0.0, 'PAX': 0.0, 'TRXBEAR': 0.0, 'TRXBULL': 0.0, 'TUSD': 0.0, 'ETHBEAR': 0.0, 'ETHBULL': 0.0, 'SNX': 0.0, 'XTZ': 0.0, 'USDJ': 0.0, 'MATIC': 0.0, 'BCHBEAR': 0.0, 'BCHBULL': 0.0, 'BSVBEAR': 0.0, 'BSVBULL': 0.0, 'BNB': 0.0, 'AVA': 0.0, 'JST': 0.0, 'BVOL': 0.0, 'IBVOL': 0.0, 'NEO': 0.0, 'SWFTC': 0.0, 'STPT': 0.0, 'FXC': 0.0, 'XRPBULL': 0.0, 'XRPBEAR': 0.0, 'EOSBULL': 0.0, 'EOSBEAR': 0.0, 'LINKBULL': 0.0, 'LINKBEAR': 0.0, 'CHR': 0.0, 'MDT': 0.0, 'BCHC': 0.0, 'COMP': 0.0, 'WRX': 0.0, 'CUSDT': 0.0, 'XFIL': 0.0, 'LEND': 0.0, 'REN': 0.0, 'LRC': 0.0, 'BAL': 0.0, 'STAKE': 0.0, 'BZRX': 0.0, 'SXP': 0.0, 'MTA': 0.0, 'YFI': 0.0, 'TRUMPWIN': 0.0, 'DEC': 0.0, 'PLT': 0.0, 'UMA': 0.0, 'KTON': 0.0, 'RING': 0.0, 'SWAP': 0.0, 'TEND': 0.0, 'TRADE': 0.0, 'GEEQ': 0.0, 'BAND': 0.0, 'DIA': 0.0, 'DOS': 0.0, 'ZAP': 0.0, 'TRB': 0.0, 'SBREE': 0.0, 'DEXT': 0.0, 'MCB': 0.0, 'PERX': 0.0, 'DOT': 0.0, 'CRV': 0.0, 'XDOT': 0.0, 'OCEAN': 0.0, 'DMG': 0.0, 'OM': 0.0, 'BLY': 0.0, 'OPT': 0.0, 'PRQ': 0.0, 'SWINGBY': 0.0, 'FUND': 0.0, 'RSR': 0.0, 'WNXM': 0.0, 'FCT2': 0.0, 'SUSHI': 0.0, 'YFII': 0.0, 'YFV': 0.0, 'YFL': 0.0, 'TAI': 0.0, 'PEARL': 0.0, 'JFI': 0.0, 'CRT': 0.0, 'SAL': 0.0, 'CORN': 0.0, 'SWRV': 0.0, 'FSW': 0.0, 'CREAM': 0.0, 'HGET': 0.0, 'AKRO': 0.0, 'ADEL': 0.0, 'UNI': 0.0, 'DHT': 0.0, 'MEME': 0.0, 'SAND': 0.0, 'CVP': 0.0, 'GHST': 0.0, 'REPV2': 0.0, 'RARI': 0.0, 'MEXP': 0.0, 'RFUEL': 0.0, 'BREE': 0.0, 'VALUE': 0.0, 'POLS': 0.0, 'AAVE': 0.0, 'BCHA': 0.0, 'BID': 0.0, 'CVT': 0.0, 'INJ': 0.0, 'WBTC': 0.0, 'SENSO': 0.0, 'KP3R': 0.0, 'MPH': 0.0, 'GLM': 0.0, 'HEGIC': 0.0, 'ZLOT': 0.0, 'NU': 0.0, 'FRONT': 0.0, 'ALPHA': 0.0, 'API3': 0.0, 'COVER': 0.0, 'ROOK': 0.0, 'BADGER': 0.0, 'FARM': 0.0, 'GRT': 0.0, 'XFLR': 0.0, 'ESD': 0.0, 'ONEINCH': 0.0, 'REEF': 0.0, 'BAS': 0.0, 'BAC': 0.0, 'LON': 0.0, 'TRU': 0.0, 'CUDOS': 0.0, 'BOND': 0.0, 'PBTC35A': 0.0, 'COMBO': 0.0, 'FTT': 0.0, 'SRM': 0.0, 'ADABEAR': 0.0, 'ADABULL': 0.0, 'LTCBEAR': 0.0, 'LTCBULL': 0.0, 'XLMBEAR': 0.0, 'XLMBULL': 0.0, 'WETH': 0.0, 'TORN': 0.0, 'ZKS': 0.0}

# Returns your balances sorted by account. You may optionally specify
# the "account" POST parameter if you wish to fetch only the balances of
# one account. Please note that balances in your margin account may not
# be accessible if you have any open margin positions or orders.

def get_available_balance(poloniex, account):
    return poloniex.returnCompleteBalances(account)

# Returns all of your balances, including available balance, balance
# on orders, and the estimated BTC value of your balance. By default,
# this call is limited to your exchange account; set the "account" POST
# parameter to "all" to include your margin and lending accounts.

def get_complete_balance(poloniex, account):
    return poloniex.returnBalances(account)

# If you are enrolled in the maker-taker fee schedule, returns your
# current trading fees and trailing 30-day volume in BTC. This
# information is updated once every 24 hours.

def get_fee(poloniex):
    return poloniex.returnFeeInfo()

# man for the poloniex api

def get_help(poloniex):
    help(poloniex)