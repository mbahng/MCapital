import matplotlib.pyplot as plt 
import numpy as np 
from import_data import * 
from utils import * 
import pandas as pd
import btalib 
import copy 
# BT stands for BackTester 

class TimeSeriesMomentumBT(object): 
    # Simple class that tells to buy based on whether returns were positive (long) or negative (short) in the past 'n' periods 
    
    def __init__(self, data_obj:tickerData, n:int=1): 
        self.ticker = copy.deepcopy(data_obj.ticker) 
        self.start_dt = copy.deepcopy(data_obj.start_dt) 
        self.end_dt = copy.deepcopy(data_obj.end_dt)
        df = copy.deepcopy(data_obj.df) 
        # log(p_{t+1}) - log(p_{t}) 
        df['change_log'] = np.log(df['average'] / df['average'].shift(1))
        df['position'] = np.sign(df['change_log'].rolling(n).mean())
        df.dropna(inplace=True)
        
        df['strategy_log'] = df['position'].shift(1) * df['change_log']
        
        df['strategy_log_cumsum'] = df['strategy_log'].cumsum()
        df['returns'] = df['strategy_log_cumsum'].apply(np.exp)
        df.dropna(inplace=True) 
        
        self.df = df 
        
    def plot_position(self): 
        simplePlot({"position" :self.df['position']}, title="Position (Long/Short)")
        
    def final_performance(self): 
        x = self.df[['change_log', 'strategy_log']].sum()
        x['change'] = np.exp(x['change_log'])
        x['strategy'] = np.exp(x['strategy_log'])
        print(x)
        
    def plot_performance(self): 
        simplePlot({"Passive Returns" : self.df['change_log'].cumsum().apply(np.exp), 
                    "Strategy Returns" : self.df['returns']}, 
                   title="Cumulative Performance")
        
class CrossSectionalMomentumBT: 
    # Given a list of tickers, we go long on companies that have recently outperformed relative to their peers and short ones that have underperformed 
    # In a given time period, we look at which company had the greatest price growth in % and invest in that one. 
    
    def __init__(self, data_pool:list, n:int=1): 
        data_pool = copy.deepcopy(data_pool)
        self.data_pool = data_pool

        for data in data_pool: 
            if type(data) != tickerData: 
                raise Exception("Some elements of data_pool are not tickerData objects. ")
            
            data.df = data.df[["average"]]
            
            data.df[f'{data.ticker} change_log'] = np.log(data.df['average'] / data.df['average'].shift(1))
            
            data.df[f'{data.ticker} % change'] = (data.df['average'] - data.df['average'].shift(n)) / data.df['average'].shift(n)
            
        
        
        df = pd.concat([data.df for data in data_pool], axis=1, ignore_index=False).sort_index()
        
        percent_change_data = df[[f"{data.ticker} % change" for data in self.data_pool]]
        for data in self.data_pool: 
            # set position to 1 if the percent change is the maximum and 0 if else 
            df[f'{data.ticker} position'] = np.where(df[f'{data.ticker} % change'] == percent_change_data.max(axis=1), 1, 0)
            df[f'{data.ticker} strategy_log'] = df[f'{data.ticker} position'].shift(1) * df[f'{data.ticker} change_log']
        
        df['strategy_log'] = sum([df[f'{data.ticker} strategy_log'] for data in self.data_pool])
        
        df.dropna(inplace=True) 
        self.df = df
        
    def plot_percentChange(self): 
        graph = self.df[[f"{data.ticker} % change" for data in self.data_pool]]
        graph.plot() 
        plt.show() 
        
    def plot_position(self): 
        graph = self.df[[f"{data.ticker} position" for data in self.data_pool]]
        graph.plot() 
        plt.show()    
        
    def plot_performance(self): 
        graph = self.df[[f"{data.ticker} change_log" for data in self.data_pool] + ["strategy_log"]]
        for column in graph.columns: 
            graph[column] = graph[column].cumsum().apply(np.exp)
           
        graph.rename(columns={col : col[:-4] for col in graph.columns}, inplace=True) 
        graph.plot() 
        plt.show() 
    
