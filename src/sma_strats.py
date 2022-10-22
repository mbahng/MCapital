import matplotlib.pyplot as plt 
import numpy as np 
from import_data import * 
from utils import * 
import pandas as pd
import btalib       # library for computing technical indicators 
import copy 

# BT stands for BackTester 

def simplePlot(name_series:dict, title=""): 
    for name, pdseries in name_series.items():
        plt.plot(pdseries, label=name)
    plt.title(title)
    plt.legend()
    plt.show() 
    
def getSMA(prices:pd.Series, period:int) -> pd.Series: 
    # Simple Moving average 
    return btalib.sma(prices, period=period).df 

def getEMA(prices:pd.Series, period:int) -> pd.Series: 
    # Exponential Moving Average 
    return btalib.ema(prices, period=period).df 

def getBollingerBands(prices:pd.Series, period:int) -> pd.Series: 
    # Returns a tuple containing upper, middle, and lower Bollinger bands for price series 
    middle_band = getSMA(prices, period) 
    upper_band = middle_band + 1.96 * prices.rolling(window=period).std() 
    lower_band = middle_band - 1.96 * prices.rolling(window=period).std() 
    
    return (upper_band, middle_band, lower_band)

# Sample code 
# x = getHourlyData("IONQ")['close']
# simplePlot({"IONQ close" : x, "IONQ close SMA300" : SMA(x, 100), "IONQ close EMA300" : EMA(x, 100)})

class SimpleMovingAverageBT(object):
    
    def __init__(self, data_obj:tickerData, sma1:int, sma2:int): 
        data = copy.deepcopy(data_obj.df) 
        self.sma1 = getSMA(data['average'], period=sma1)   # smaller sma
        self.sma2 = getSMA(data['average'], period=sma2)   # bigger sma 
        data['SMA1'] = self.sma1 
        data['SMA2'] = self.sma2 
        
        # Go long (1) if the smaller sma is greater than bigger sma
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data.dropna(inplace=True)
        data['change_log'] = np.log(data['average'] / data['average'].shift(1))

        data['strategy_log'] = data['position'].shift(1) * data['change_log']
        data.dropna(inplace=True)
        self.df = data 
        
    def final_performance(self): 
        print(self.df[['change_log', 'strategy_log']].sum().apply(np.exp))
            
    def plot_position(self): 
        simplePlot({"position" : self.df["position"]}, 
                   title="Position (Long/Short)")
        
    def plot_performance(self): 
        simplePlot({"Passive Returns" : self.df['change_log'].cumsum().apply(np.exp), 
                    "Strategy Returns" : self.df['strategy_log'].cumsum().apply(np.exp)}, 
                   title="Cumulative Performance")
        
    def plot_SMA(self): 
        simplePlot({"Stock" : self.df['average'], 
                    "SMA1" : self.df['SMA1'], 
                    'SMA2' : self.df['SMA2']}, 
                   title="Stock vs SMAs")
    


