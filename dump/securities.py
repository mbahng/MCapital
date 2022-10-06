import datetime as dt
import numpy as np 
from abc import ABC, abstractmethod 
import yfinance as yf 

def current_price(tick:str): 
    return yf.Ticker(tick).info['regularMarketPrice']

class Investor: 
    def __init__(self, name:str, cash:float, portfolio:dict={}): 
        self.name = name 
        self.cash = cash 
        self.total_value = cash
        self.initial_investment = cash
        self.portfolio = portfolio 
        
        
    def buy(self, tick:str, no_shares:int, buy_price:float=None): 
        
        if buy_price == None: 
            buy_price = current_price(tick)
        
        if tick not in self.portfolio: 
            self.portfolio[tick] = []
        
        self.portfolio[tick] += [ Stock(tick, buy_price) for _ in range(no_shares)]
        
        self.cash -= no_shares * buy_price
        
    def sell(self, tick:str, no_shares:int, sell_price:float): 
        
        if tick not in self.portfolio: 
            raise Exception("You do not own this stock to sell. ")
        if no_shares > len(self.portfolio[tick]): 
            raise Exception("You cannot sell more than you already have. ")
        
        self.portfolio[tick] = self.portfolio[tick][no_shares:]
        
        self.cash += no_shares * sell_price
        
    def close_position(self, tick:str): 
        self.sell(tick, len(self.portfolio[tick]), current_price(tick))
        
    def portfolio_value(self): 
        return self.cash + sum([current_price(tick) * len(self.portfolio[tick]) for tick in self.portfolio])
    
    def profit_summary(self): 
        print(f"Initial Investment: {self.initial_investment}") 
        print(f"Current Portfolio Value: {self.portfolio_value()}")        
        

class Stock: 
    def __init__(self, tick, buy_price): 
        self.tick = tick 
        self.buy_price = buy_price 
        