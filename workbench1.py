from re import T
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

# errored = []
# for ticker in sp100_yahoo[5:]: 
#     try: 
#         importStockData(ticker, daily=True, hourly=True, minutely=False)
#     except: 
#         errored.append(ticker) 
#         print(f"ERRORED: {ticker}")

x = getDailyStockData('IONQ').df
y = getDailyStockData('DD').df
print(y)

z = pd.concat([x, y], axis=1, ignore_index=False)
z = z.sort_index()
print(z)