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

data = getDailyStockData("DD")
back = SMABackTester(data, 42, 252)
back.final_performance() 
back.plot_position()
back.plot_SMA()
back.plot_performance() 