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

c1 = "T" 
c2 = "VZ"

# importDailyStockData(c1) 
# importDailyStockData(c2)
# assert False

df1 = getDailyStockData(c1).df
df1.rename(columns={'average' : 'average1'}, inplace=True)
df2 = getDailyStockData(c2).df
df2.rename(columns={'average' : 'average2'}, inplace=True)


df_comb = pd.concat([df1, df2], axis=1).dropna()
df_comb['ratio'] = df_comb['average1'] / df_comb['average2']
print(df_comb)

df_comb['ratio'].plot()
plt.show()