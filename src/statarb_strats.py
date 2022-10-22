import matplotlib.pyplot as plt 
import numpy as np 
from import_data import * 
from utils import * 
import pandas as pd
import copy 
import seaborn as sns

def correlationDetector(tickerData_list:list, n_back:int=100, cutoff=0.85):
    # returns a pandas series with indices as tuples of stock tickers 
    # and values as correlations, ranked from highest to lowest
    def rename(td:tickerData): 
        return td.df[['average']].rename(columns={'average' : td.ticker})
    
    df = pd.concat([rename(td) for td in tickerData_list], axis=1).dropna()
    df = df.tail(n_back)
    corr_matrix = df.corr() 
    highest_corr = corr_matrix.unstack().sort_values(kind='quicksort', ascending=False)[len(tickerData_list)::2]
    
    # keep only ones with correlation greater than 'cutoff'
    highest_corr = highest_corr[highest_corr > cutoff]
    
    return highest_corr

class PairsTradingBT(object): 
    
    def __init__(self, data_obj1:tickerData, data_obj2:tickerData, n_back:int=100, n_std_dev:float=2.0): 
        c1 = data_obj1.ticker 
        c2 = data_obj2.ticker
        
        df1 = data_obj1.df.rename(columns={'average' : data_obj1.ticker})
        df2 = data_obj2.df.rename(columns={'average' : data_obj2.ticker})
        
        df_comb = pd.concat([df1, df2], axis=1).dropna()
        df_comb['color'] = range(len(df_comb[data_obj1.ticker]))
        df_comb = df_comb.tail(n_back)
        d = np.polyfit(df_comb[c1], df_comb[c2], 1)     # linear regression 
        df_comb[f'scaled_{c1}'] = d[0] * df_comb[c1] + d[1] 
        df_comb['scaled_diff'] = df_comb[c2] - df_comb[f'scaled_{c1}']
        
        self.ticker1 = c1 
        self.ticker2 = c2
        self.df = df_comb 
        self.n_back = n_back
        self.n_std_dev = n_std_dev
        
        mean = self.df['scaled_diff'].mean()        # should be 0 
        std_dev = self.df['scaled_diff'].std()
        self.upper_signal = mean + self.n_std_dev * std_dev 
        self.lower_signal = mean - self.n_std_dev * std_dev 
        
    def plotScatter(self): 
        self.df.plot.scatter(x=self.ticker1, y=self.ticker2, s=1, c="color", colormap="viridis")
        plt.show() 
        
    def plotDifference(self): 
        self.df['scaled_diff'].plot(c="b", label=f"Daily: {self.ticker2}-{self.ticker1}")
        plt.axhline(y=self.upper_signal, color='g', linestyle='-', label=f"{self.n_std_dev} std (Long {self.ticker1}, Short {self.ticker2})")
        plt.axhline(y=self.lower_signal, color='r', linestyle='-', label=f"{self.n_std_dev} std (Long {self.ticker2}, Short {self.ticker1})")
        plt.legend() 
        plt.show() 
        
    def histogramDifference(self): 
        self.df['scaled_diff'].hist(label=f"Daily: {self.ticker2}-{self.ticker1}", grid=False, bins=int(round(self.n_back/100)))
        plt.axvline(x=self.upper_signal, color='g', linestyle='-', label=f"{self.n_std_dev} std (Long {self.ticker1}, Short {self.ticker2})")
        plt.axvline(x=self.lower_signal, color='r', linestyle='-', label=f"{self.n_std_dev} std (Long {self.ticker2}, Short {self.ticker1})")
        plt.legend() 
        plt.show() 
        
    def position(self): 
        last_diff = self.df['scaled_diff'].iloc[-1]
        if last_diff < self.lower_signal: 
            print(f"Current Difference ({self.ticker2}-{self.ticker1}) of {last_diff} is smaller than Lower Signal of {self.lower_signal}: \n LONG {self.ticker2}, SHORT {self.ticker1}") 
            pass 
        elif last_diff > self.upper_signal: 
            print(f"Current Difference ({self.ticker2}-{self.ticker1}) of {last_diff} is greater than Upper Signal of {self.upper_signal}: \n LONG {self.ticker1}, SHORT {self.ticker2}") 
            pass 
        else: 
            # print(f"Current Difference ({self.ticker2}-{self.ticker1}) of {last_diff} is between Lower Signal of {self.lower_signal} and Upper Signal of {self.upper_signal}. \n DO NOTHING ")
            pass 
            
def scanForPairTradingOpps(no_days_back:int=1000, correlation_cutoff:float=0.8, n_std_dev:float=2.0): 
    all_tickerData = [getDailyStockData(file[:-5]) for file in os.listdir("database/stocks")]

    corrs = correlationDetector(all_tickerData, 
                                cutoff=correlation_cutoff)

    for i in range(len(corrs.index)): 
        c1, c2 = corrs.index[i]

        x = PairsTradingBT(getDailyStockData(c1), 
                        getDailyStockData(c2), 
                        n_back=no_days_back, 
                        n_std_dev=n_std_dev) 
        x.position()