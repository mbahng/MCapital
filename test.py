import sqlite3
import pandas as pd
from ib_insync import * 
from random import randint
from datetime import *

ib = IB() 
ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

stock = Stock("RIVN", "SMART", "USD") 

bars = ib.reqHistoricalData(
        stock, endDateTime='', durationStr="10 Y", 
        barSizeSetting="1 day", whatToShow="TRADES", useRTH=False, formatDate=2, 
        timeout=0)

df = util.df(bars)

print(df)

assert False

for index, row in df.iterrows(): 
    c.execute(f"INSERT INTO hourly VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
    
conn.commit() 

conn.close() 

ib.disconnect() 
ib.waitOnUpdate(timeout=0.5)