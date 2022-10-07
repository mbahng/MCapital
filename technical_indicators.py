from cProfile import label
import matplotlib.pyplot as plt 
from import_data import * 
import pandas as pd
import btalib       # library for computing technical indicators 

def simplePlot(name_series:dict): 
    for name, pdseries in name_series.items():
        plt.plot(pdseries, label=name)
    plt.legend()
    plt.show() 
    
def SMA(prices:pd.Series, period): 
    return btalib.sma(prices, period=period).df 

def EMA(prices:pd.Series, period): 
    return btalib.ema(prices, period=period).df
    
x = getHourlyData("IONQ")['close']
y = getHourlyData('RGTI')['close']
simplePlot({"IONQ close" : x, "IONQ close SMA300" : SMA(x, 100), "IONQ close EMA300" : EMA(x, 100)})

