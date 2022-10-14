import matplotlib.pyplot as plt 
import numpy as np

from import_data import tickerData 

def simplePlot(tickerDataList:list, title=""): 
    for company in tickerDataList: 
        plt.plot(company.df['average'], label=company.ticker)
    plt.title(title)
    plt.legend()
    plt.show() 