import sqlite3, time
from ib_insync import * 
import pandas as pd, numpy as np 
from random import randint
from datetime import *

import sys 
sys.path.insert(1, "src")           # add directory to python path 
sys.path.insert(1, "database")      # add directory to python path 
from import_data import * 
from sma_strats import * 
from momentum_strats import * 
from statarb_strats import * 
from utils import * 
from tickers import * 

ib = IB() 
ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

stock = Stock("IONQ", "SMART", "USD", primaryExchange="NASDAQ")
order = LimitOrder('BUY', 20, 4.95, outsideRth=True) 

ib.placeOrder(stock, order) 

ib.sleep(2) 

print(len(ib.trades()), len(ib.orders()))

print(ib.trades()) 
print(ib.orders())
