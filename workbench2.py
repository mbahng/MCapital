import sqlite3, time
from ib_insync import * 
import pandas as pd, numpy as np 
from random import randint
from datetime import *

import sys

from sklearn.model_selection import GridSearchCV 
sys.path.insert(1, "src")           # add directory to python path 
sys.path.insert(1, "database")      # add directory to python path 
from import_data import * 
from sma_strats import * 
from momentum_strats import * 
from statarb_strats import * 
from utils import * 
from tickers import * 

import matplotlib.pyplot as plt 
import sklearn 
from sklearn.datasets import load_boston 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.pipeline import Pipeline 

X, y = load_boston(return_X_y=True) 

# Initialize pipeline object containing model and scaler 
pipe = Pipeline([
    ("scale", RobustScaler()), 
    ("model", KNeighborsRegressor(n_neighbors=5))
])

# Divide up the data into a training set and predicting set to perform cross-validation. 
# Check all combinations of hyperparameters, in this case exhaustively using GridSearchCV 
mod = GridSearchCV(estimator = pipe, 
                   param_grid = {'model__n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, 
                   cv = 3)  # divides the data into cv batches, with cv-1 training  

mod.fit(X, y)      # train the model

results = mod.cv_results_ 
print(pd.DataFrame(results)) 

assert False 
pred = pipe.predict(X) 

print(pred) 

plt.scatter(y, pred, s=1)
plt.show() 