from re import T
import sqlite3, time
from ib_insync import * 
import pandas as pd, numpy as np 
from random import randint
from datetime import *
import os 

import sys 
sys.path.insert(1, "src")           # add directory to python path 
sys.path.insert(1, "database")      # add directory to python path 
from import_data import * 
from sma_strats import * 
from momentum_strats import * 
from statarb_strats import * 
from utils import * 
import seaborn as sns 
from itertools import combinations 

# scanForPairTradingOpps(no_days_back=300, 
#                        correlation_cutoff=0.90, 
#                        n_std_dev=4.0) 

tkd = getDailyStockData("DIS") 
tkd.addIchimoku()
print(tkd.df)

tkd.plot(ichimoku=True)