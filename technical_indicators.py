from cProfile import label
import matplotlib.pyplot as plt 
from import_data import * 
import pandas as pd
import btalib       # library for computing technical indicators 

df = getDailyData("IONQ")
sma30 = btalib.sma(df, period=30) 
sma100 = btalib.sma(df, period=100)
sma300 = btalib.sma(df, period=300)


ax = df["close"].plot() 
sma30.df.plot(ax=ax, label="sma30")
sma100.df.plot(ax=ax, label="sma100")
sma300.df.plot(ax=ax, label="sma300")
plt.show()