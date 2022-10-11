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

data_pool = [getDailyStockData('IONQ'), 
             getDailyStockData('RGTI')]

x = CrossSectionalMomentumBT(data_pool, 1)

x.plot_performance()
