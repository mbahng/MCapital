from ib_insync import * 
from database.tickers import * 
from random import randint
from datetime import datetime as dt
import os.path
import pandas as pd


def importDailyStockData(ticker:str): 
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='6 M',
                barSizeSetting="1 day",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='1 Y',
                barSizeSetting="1 day",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 
    
    df = df.set_index("date")
    df = df.drop('barCount', axis=1)
    df = df[~df.index.duplicated(keep="first")]
    print(df)

    # write into hdf5 file
    df.to_hdf(f"database/stocks/{ticker}.hdf5", "daily")
    
    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)

def importHourlyStockData(ticker:str): 
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
        
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='6 M',
                barSizeSetting="1 hour",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='1 Y',
                barSizeSetting="1 hour",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 

    df = df.set_index("date")
    df = df.drop('barCount', axis=1)
    df = df[~df.index.duplicated(keep="first")]
    print(df)
    # write into hdf5 file
    df.to_hdf(f"database/stocks/{ticker}.hdf5", "hourly")
    
    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)

def importMinutelyStockData(ticker:str): 
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
        
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='1 M',
                barSizeSetting="1 min",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        
        dt = ''
        barsList = []
        while True:
            bars = ib.reqHistoricalData(
                stock, endDateTime=dt, durationStr='1 M',
                barSizeSetting="1 min",whatToShow='TRADES',
                useRTH=False, formatDate=2, timeout=0)
            if not bars:
                break
            if dt == bars[0].date: 
                break 
            barsList.append(bars)
            dt = bars[0].date
            print(dt)

        # convert to pandas dataframe 
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars) 

    df = df.set_index("date")
    df = df.drop('barCount', axis=1)
    df = df[~df.index.duplicated(keep="first")]
    print(df)
    # write into hdf5 file
    df.to_hdf(f"database/stocks/{ticker}.hdf5", "minutely")
    
    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)

def importStockData(ticker:str, daily:bool, hourly:bool, minutely:bool): 
    if daily == True: 
        importDailyStockData(ticker) 
    if hourly == True: 
        importHourlyStockData(ticker) 
    if minutely == True: 
        importMinutelyStockData(ticker) 

def importAllStockData(ticker:str): 
    importStockData(ticker, daily=True, hourly=True, minutely=True)


def updateDailyStockData(ticker:str): 
    no_weeks_back = 1
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

    # check if this file exists
    if os.path.isfile(f'database/stocks/{ticker}.hdf5') == False: 
        raise Exception("This file does not exist. ")

    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "daily")
    df.drop(df.tail(3).index, inplace=True)

    last_recorded_date = df.tail(1).index[0]
    print("Updating Data After: " + str(last_recorded_date))

    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
        ib.reqMktData(stock, '', False, False) 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NASDAQ") 
        ib.reqMktData(stock, '', False, False) 
    
    bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 day", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

    df_add = util.df(bars)
    df_add = df_add.set_index("date")
    
    while df_add.index[0] > df.index[-1]: 
        no_weeks_back += 1 
        
        bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 day", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

        df = util.df(bars)
        df_add = df_add.set_index("date")
    
    # truncate the first few datetimes until we find appropriate place to add to 
    df_add = df_add[df_add.index > last_recorded_date].drop(columns=['barCount'])
    df_updated = pd.concat([df, df_add], axis=0)
    df_updated = df_updated[~df_updated.index.duplicated(keep="first")]     # delete all rows with duplicate indices

    df_updated.to_hdf(f"database/stocks/{ticker}.hdf5", "daily")
        
    print(f"===== Stock {ticker} Daily Price Updated =====")
    print(df_updated)   
    print(f"===== Stock {ticker} Daily Price Updated =====\n")

    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)
    
def updateHourlyStockData(ticker:str): 
    no_weeks_back = 1
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

    # check if this file exists
    if os.path.isfile(f'database/stocks/{ticker}.hdf5') == False: 
        raise Exception("This file does not exist. ")

    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "hourly")
    df.drop(df.tail(3).index, inplace=True)
    last_recorded_date = df.tail(1).index[0]
    print("Updating Data After: " + str(last_recorded_date))

    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NASDAQ") 
    
    bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 hour", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

    df_add = util.df(bars)
    df_add = df_add.set_index("date")
    
    while df_add.index[0] > df.index[-1]: 
        no_weeks_back += 1 
        
        bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 hour", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

        df = util.df(bars)
        df_add = df_add.set_index("date")
    
    # truncate the first few datetimes until we find appropriate place to add to 
    df_add = df_add[df_add.index > last_recorded_date].drop(columns=['barCount'])
    df_updated = pd.concat([df, df_add], axis=0)
    df_updated = df_updated[~df_updated.index.duplicated(keep="first")]

    df_updated.to_hdf(f"database/stocks/{ticker}.hdf5", "hourly")
        
    print(f"===== Stock {ticker} Hourly Price Updated =====")
    print(df_updated) 
    print(f"===== Stock {ticker} Hourly Price Updated =====\n")

    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)
        
def updateMinutelyStockData(ticker:str): 
    no_weeks_back = 1
    
    ib = IB() 
    ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

    # check if this file exists
    if os.path.isfile(f'database/stocks/{ticker}.hdf5') == False: 
        raise Exception("This file does not exist. ")

    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "minutely")
    df.drop(df.tail(3).index, inplace=True)
    last_recorded_date = df.tail(1).index[0]
    print("Updating Data After: " + str(last_recorded_date))

    try: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NYSE") 
    except: 
        stock = Stock(ticker, "SMART", "USD", primaryExchange="NASDAQ") 
    
    bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 min", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

    df_add = util.df(bars)
    df_add = df_add.set_index("date")
    
    while df_add.index[0] > df.index[-1]: 
        no_weeks_back += 1 
        
        bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
            barSizeSetting="1 min", whatToShow="TRADES", useRTH=False, formatDate=2, 
            timeout=0)

        df = util.df(bars)
        df_add = df_add.set_index("date")
    
    # truncate the first few datetimes until we find appropriate place to add to 
    df_add = df_add[df_add.index > last_recorded_date].drop(columns=['barCount'])
    df_updated = pd.concat([df, df_add], axis=0)
    df_updated = df_updated[~df_updated.index.duplicated(keep="first")]

    df_updated.to_hdf(f"database/stocks/{ticker}.hdf5", "minutely")
        
    print(f"===== Stock {ticker} Minutely Price Updated =====")
    print(df_updated) 
    print(f"===== Stock {ticker} Minutely Price Updated =====\n")

    ib.disconnect() 
    ib.waitOnUpdate(timeout=0.5)
         
def updateStockData(ticker:str, daily:bool, hourly:bool, minutely:bool): 
    if daily == True: 
        updateDailyStockData(ticker) 
    if hourly == True: 
        updateHourlyStockData(ticker) 
    if minutely == True: 
        updateMinutelyStockData(ticker) 

def updateAllStockData(ticker:str): 
    updateStockData(ticker, daily=True, hourly=True, minutely=True)

class tickerData: 
    def __init__(self, df, ticker): 
        self.df = df 
        self.ticker = ticker 
        self.start_dt = df.index[0] 
        self.end_dt = df.index[-1] 

def getDailyStockData(ticker:str): 
    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "daily")
    return tickerData(df, ticker)

def getHourlyStockData(ticker:str): 
    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "hourly")
    return tickerData(df, ticker) 

def getMinutelyStockData(ticker:str): 
    df = pd.read_hdf(f"database/stocks/{ticker}.hdf5", "minutely")
    return tickerData(df, ticker)


# Functions for SQLite database 

# def importDailyStockData(ticker:str): 
    
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
#     try: 
#         stock = Stock(ticker, "SMART", "USD") 
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='6 M',
#                 barSizeSetting="1 day",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             if dt == bars[0].date: 
#                 break 
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)
#     except: 
#         stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='1 Y',
#                 barSizeSetting="1 day",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)

#     # connect to relevant database and create one if doesn't exist
#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')

#     c = conn.cursor() 
    
#     try:    # create a table if it doesn't exist 
#         c.execute(f"""CREATE TABLE daily (
#                     date text, 
#                     open real, 
#                     high real, 
#                     low real, 
#                     close real, 
#                     volume integer, 
#                     average real
#                     )""")
#         conn.commit() 
#     except: 
#         pass 


#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO daily VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
#     conn.commit() 

#     conn.close() 
#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5)

# def importHourlyStockData(ticker:str): 
    
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
#     try: 
#         stock = Stock(ticker, "SMART", "USD") 
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='6 M',
#                 barSizeSetting="1 hour",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)
#     except: 
#         stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='1 Y',
#                 barSizeSetting="1 hour",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)

#     # connect to relevant database and create one if doesn't exist
#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')

#     c = conn.cursor() 
    
#     try:    # create a table if it doesn't exist 
#         c.execute(f"""CREATE TABLE hourly (
#                     date text, 
#                     open real, 
#                     high real, 
#                     low real, 
#                     close real, 
#                     volume integer, 
#                     average real
#                     )""")
#         conn.commit() 
#     except: 
#         pass 


#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO hourly VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
#     conn.commit() 

#     conn.close() 
#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5)

# def importMinutelyStockData(ticker:str): 
    
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
#     try: 
#         stock = Stock(ticker, "SMART", "USD") 
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='1 M',
#                 barSizeSetting="1 min",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)
#     except: 
#         stock = Stock(ticker, "SMART", "USD", primaryExchange='NASDAQ')
        
#         dt = ''
#         barsList = []
#         while True:
#             bars = ib.reqHistoricalData(
#                 stock, endDateTime=dt, durationStr='1 M',
#                 barSizeSetting="1 min",whatToShow='TRADES',
#                 useRTH=False, formatDate=2, timeout=0)
#             if not bars:
#                 break
#             barsList.append(bars)
#             dt = bars[0].date
#             print(dt)

#         # convert to pandas dataframe 
#         allBars = [b for bars in reversed(barsList) for b in bars]
#         df = util.df(allBars) 
#         print(df)

#     # connect to relevant database and create one if doesn't exist
#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')

#     c = conn.cursor() 
    
#     try:    # create a table if it doesn't exist 
#         c.execute(f"""CREATE TABLE minutely (
#                     date text, 
#                     open real, 
#                     high real, 
#                     low real, 
#                     close real, 
#                     volume integer, 
#                     average real
#                     )""")
#         conn.commit() 
#     except: 
#         pass 


#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO minutely VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
#     conn.commit() 

#     conn.close() 
#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5)

# def importStockData(ticker:str, daily:bool, hourly:bool, minutely:bool): 
#     if daily == True: 
#         importDailyStockData(ticker) 
#     if hourly == True: 
#         importHourlyStockData(ticker) 
#     if minutely == True: 
#         importMinutelyStockData(ticker) 

# def importAllStockData(ticker:str): 
#     importStockData(ticker, daily=True, hourly=True, minutely=True)


# def updateDailyStockData(ticker:str): 
#     no_weeks_back = 1
    
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 

#     # check if this file exists
#     if os.path.isfile(f'database/Stocks/{ticker}.db') == False: 
#         raise Exception("This file does not exist. ")
    
#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')

#     c = conn.cursor() 

#     # delete last 3 rows, which may need to be updated. 
#     c.execute('''DELETE FROM daily WHERE date IN 
#             (SELECT date FROM daily ORDER BY date DESC LIMIT 3)''')
#     conn.commit() 

#     # get datetime of last row
#     last_recorded_date = c.execute(f"SELECT * FROM daily ORDER BY date DESC LIMIT 1;").fetchall()[-1][0]
#     print("Updating Data From: " + last_recorded_date)

#     stock = Stock(ticker, "SMART", "USD") 
    
#     bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
#             barSizeSetting="1 day", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)

#     df = util.df(bars)
    
#     while df['date'][0] > dt.strptime(last_recorded_date, "%Y-%m-%d").date(): 
#         no_weeks_back += 1 
        
#         bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
#             barSizeSetting="1 day", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)

#         df = util.df(bars)
    
#     # find the datetime where we should update from 
    
#     index = df.date[df.date == dt.strptime(last_recorded_date, "%Y-%m-%d").date()].index[0]
    
#     df = df.iloc[index+1: , :]
    
#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO daily VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
#     conn.commit()    
#     print(f"===== Stock {ticker} Daily Price Updated =====")
#     print(df.head(3))
#     print(df.tail(3))
#     print(f"===== Stock {ticker} Daily Price Updated =====\n")
    
#     conn.close()
#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5)

# def updateHourlyStockData(ticker:str): 
#     no_weeks_back = 1
    
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
#     # check if this file exists
#     if os.path.isfile(f'database/Stocks/{ticker}.db') == False: 
#         raise Exception("This file does not exist. ")

#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')

#     c = conn.cursor() 

#     # delete last 3 rows, which may need to be updated. 
#     c.execute('''DELETE FROM hourly WHERE date IN 
#             (SELECT date FROM hourly ORDER BY date DESC LIMIT 3)''')
#     conn.commit() 

#     # get datetime of last row
#     last_recorded_date = c.execute(f"SELECT * FROM hourly ORDER BY date DESC LIMIT 1;").fetchall()[-1][0]
#     print("Updating Data From: " + last_recorded_date)

#     stock = Stock(ticker, "SMART", "USD") 
    
#     bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
#             barSizeSetting="1 hour", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)

#     df = util.df(bars)
    
#     while df['date'][0] > dt.strptime(last_recorded_date, "%Y-%m-%d %H:%M:%S%z"): 
#         no_weeks_back += 1 
        
#         bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
#             barSizeSetting="1 hour", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)

#         df = util.df(bars)
    
#     # find the datetime where we should update from 
    
#     index = df.date[df.date == dt.strptime(last_recorded_date, "%Y-%m-%d %H:%M:%S%z")].index[0]
    
#     df = df.iloc[index+1: , :]
    
#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO hourly VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
        
#     print(f"===== Stock {ticker} Hourly Price Updated =====")
#     print(df.head(3))
#     print(df.tail(3))
#     print(f"===== Stock {ticker} Hourly Price Updated =====\n")
    
#     conn.commit() 

#     conn.close() 

#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5)
        
# def updateMinutelyStockData(ticker:str): 
#     # start off by trying to update 1 week back 
#     # May need to go further back if we haven't updated in a while
#     no_weeks_back = 1   
    
#     # Connect to Interactive brokers
#     ib = IB() 
#     ib.connect('127.0.0.1', 7497, clientId=randint(0, 9999), timeout=0) 
    
#     # check if this file exists
#     if os.path.isfile(f'database/Stocks/{ticker}.db') == False: 
#         raise Exception("This file does not exist. ")

#     # Access the SQL database for relevant company
#     conn = sqlite3.connect(f'database/Stocks/{ticker}.db')
#     c = conn.cursor() 

#     # delete last 3 rows of DB, since they may contain incomplete data 
#     c.execute('''DELETE FROM minutely WHERE date IN 
#                 (SELECT date FROM minutely ORDER BY date DESC LIMIT 3)''')
#     conn.commit() 

#     # get datetime of last row of current DB
#     last_recorded_date = c.execute(f"SELECT * FROM minutely ORDER BY date DESC LIMIT 1;").fetchall()[-1][0]
#     print("Updating Data From: " + last_recorded_date)

#     # Request historical data back to 1 week and put it in a pandas dataframe. 
#     stock = Stock(ticker, "SMART", "USD") 
#     bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} W", 
#             barSizeSetting="1 min", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)
#     df = util.df(bars)
     
#     # while we haven't updated far enough, add another week and get historical data again
#     while df['date'][0] > dt.strptime(last_recorded_date, "%Y-%m-%d %H:%M:%S%z"): 
#         no_weeks_back += 1 
        
#         bars = ib.reqHistoricalData(
#             stock, endDateTime='', durationStr=f"{no_weeks_back} D", 
#             barSizeSetting="1 min", whatToShow="TRADES", useRTH=False, formatDate=2, 
#             timeout=0)

#         df = util.df(bars)
    
#     # find the exact datetime where we should update from and cut off all previous data
#     index = df.date[df.date == dt.strptime(last_recorded_date, "%Y-%m-%d %H:%M:%S%z")].index[0]
#     df = df.iloc[index+1: , :]
    
#     # add the new data to the database 
#     for index, row in df.iterrows(): 
#         c.execute(f"INSERT INTO minutely VALUES ('{str(row['date'])}', {row['open']}, {row['high']}, {row['low']}, {row['close']}, {int(row['volume'])}, {row['average']})")
#     conn.commit()
    
#     print(f"===== Stock {ticker} Minutely Price Updated =====")
#     print(df.head(3))
#     print(df.tail(3))
#     print(f"===== Stock {ticker} Minutely Price Updated =====\n")
    
#     # Close connections 
#     conn.close() 
#     ib.disconnect() 
#     ib.waitOnUpdate(timeout=0.5) 
    
# def updateStockData(ticker:str, daily:bool, hourly:bool, minutely:bool): 
#     if daily == True: 
#         updateDailyStockData(ticker) 
#     if hourly == True: 
#         updateHourlyStockData(ticker) 
#     if minutely == True: 
#         updateMinutelyStockData(ticker) 

# def updateAllStockData(ticker:str): 
#     updateStockData(ticker, daily=True, hourly=True, minutely=True)


# def getDailyStockData(ticker:str): 
#     cnx = sqlite3.connect(f"database/Stocks/{ticker}.db") 
#     df = pd.read_sql_query("SELECT * FROM daily", cnx)
#     df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
#     df = df.set_index("date") 
#     return df 

# def getHourlyStockData(ticker:str): 
#     cnx = sqlite3.connect(f"database/Stocks/{ticker}.db") 
#     df = pd.read_sql_query("SELECT * FROM hourly", cnx)
#     df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z")
#     df = df.set_index("date") 
#     return df 

# def getMinutelyStockData(ticker:str): 
#     cnx = sqlite3.connect(f"database/Stocks/{ticker}.db") 
#     df = pd.read_sql_query("SELECT * FROM minutely", cnx)
#     df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z")
#     df = df.set_index("date") 
#     return df 