import matplotlib.pyplot as plt 
import numpy as np 

def simplePlot(name_series:dict, title=""): 
    for name, pdseries in name_series.items():
        plt.plot(pdseries, label=name)
    plt.title(title)
    plt.legend()
    plt.show() 