import matplotlib.pyplot as plt 
import numpy as np 
from import_data import * 
import pandas as pd
import btalib       # library for computing technical indicators 

def simplePlot(name_series:dict, title=""): 
    for name, pdseries in name_series.items():
        plt.plot(pdseries, label=name)
    plt.title(title)
    plt.legend()
    plt.show() 
    
def SMA(prices:pd.Series, period): 
    return btalib.sma(prices, period=period).df 

def EMA(prices:pd.Series, period): 
    return btalib.ema(prices, period=period).df

# Sample code 
# x = getHourlyData("IONQ")['close']
# simplePlot({"IONQ close" : x, "IONQ close SMA300" : SMA(x, 100), "IONQ close EMA300" : EMA(x, 100)})

class SMABackTester(object):
    
    def __init__(self, data:pd.Series, sma1:int, sma2:int): 
        self.sma1 = SMA(data['average'], period=sma1)   # smaller sma
        self.sma2 = SMA(data['average'], period=sma2)   # bigger sma 
        data['SMA1'] = self.sma1 
        data['SMA2'] = self.sma2 
        
        # Go long (1) if the smaller sma is greater than bigger sma
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data.dropna(inplace=True)
        data['log_returns'] = np.log(data['average'] / data['average'].shift(1))

        data['strategy'] = data['position'].shift(1) * data['log_returns']
        data.dropna(inplace=True)
        self.data = data 
        
    def final_performance(self): 
        print(self.data[['log_returns', 'strategy']].sum().apply(np.exp))
            
    def plot_position(self): 
        simplePlot({"position" : self.data["position"]}, 
                   title="Position (Long/Short)")
        
    def plot_performance(self): 
        simplePlot({"Passive Returns" : self.data['log_returns'].cumsum().apply(np.exp), 
                    "Strategy Returns" : self.data['strategy'].cumsum().apply(np.exp)}, 
                   title="Cumulative Performance")
        
    def plot_SMA(self): 
        simplePlot({"Stock" : self.data['average'], 
                    "SMA1" : self.data['SMA1'], 
                    'SMA2' : self.data['SMA2']}, 
                   title="Stock vs SMAs")
    


