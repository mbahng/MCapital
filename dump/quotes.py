import yfinance as yf 

def current_price(tick:str): 
    return yf.Ticker(tick).info['regularMarketPrice']