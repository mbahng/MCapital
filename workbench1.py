import sqlite3, time
from ib_insync import * 
import pandas as pd, numpy as np 
from random import randint
from datetime import *

import sys 
sys.path.insert(1, "src")           # add directory to python path 
sys.path.insert(1, "database")      # add directory to python path 
from import_data import * 
from technical_indicators import * 
from tickers import * 


# d = getHourlyStockData("DD")['average']
# simplePlot({"DD Avg" : d, "SMA100" : SMA(d, period=100), "SMA300" : SMA(d, period=300)})
for ticker in sp100_yahoo: 
    