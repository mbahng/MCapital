from btalib import sma, ema
import numpy as np, pandas as pd 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go  

class tickerData: 
    def __init__(self, df, ticker): 
        self.df = df 
        self.ticker = ticker 
        self.start_dt = df.index[0] 
        self.end_dt = df.index[-1] 

    def addSimpleMovingAvg(self, period:int, OHLC:str="close"): 
        self.df[f"SMA"] = sma(self.df[OHLC], period=period).df 
        return self.df

    def addExponentialMovingAvg(self, period:int, OHLC:str="close"): 
        self.df[f"EMA"] = ema(self.df[OHLC], period=period).df 
        return self.df 
    
    def addBollingerBands(self, period:int, OHLC:str="close"): 
        # Middle band is simple moving average 
        # Upper band and lower band is 1.96 standard deviations away from middle band
        middle_band = sma(self.df[OHLC], period=period).df['sma']
        std_dev = 1.96 * self.df[OHLC].rolling(window=period).std()
        self.df[f"Lower_Bollinger"] = middle_band - std_dev 
        self.df[f"Middle_Bollinger"] = middle_band
        self.df[f"Upper_Bollinger"] = middle_band + std_dev
        return self.df 
    
    def addIchimoku(self): 
        # Conversion line = (Highest Value in period + Lowest value in period)/2 (9 sessions) 
        hi_val = self.df['high'].rolling(window=9).max() 
        lo_val = self.df['low'].rolling(window=9).min() 
        self.df['Conversion'] = (hi_val + lo_val) / 2
        
        # Base Line = (Highest Value in period + Lowest Value in period)/2 (26 sessions) 
        hi_val2 = self.df['high'].rolling(window=26).max() 
        lo_val2 = self.df['low'].rolling(window=26).min() 
        self.df['Baseline'] = (hi_val2 + lo_val2) / 2
        
        # Span A = (Conversion Value + Base Value)/2 (26 sessions) 
        self.df['SpanA'] = ((self.df['Conversion'] + self.df['Baseline']) / 2)
        
        # Span B = (Conversion Value + Base Value)/2 (52 sessions) 
        hi_val3 = self.df['high'].rolling(window=52).max() 
        lo_val3 = self.df['low'].rolling(window=52).min() 
        self.df['SpanB'] = ((hi_val3 + lo_val3) / 2).shift(26)
        
        # Lagging Span = Price shifted back 26 periods 
        self.df['Lagging'] = self.df['close'].shift(-26)
        
        return self.df
    
    def plot(self, sma=False, ema=False, bollinger=False, ichimoku=False):
        fig = go.Figure() 
        
        candle = go.Candlestick(x=self.df.index, 
                                open = self.df['open'], 
                                high= self.df['high'], 
                                low = self.df['low'], 
                                close = self.df['close'], 
                                name = 'Candlestick')
        
        fig.add_trace(candle) 
        
        if sma == True: 
            try: 
                sma = go.Scatter(x=self.df.index, y = self.df['SMA'], line=dict(color="rgba(0, 0, 250, 0.75)", width=1), name="SMA")
                fig.add_trace(sma)
            except: 
                raise Exception("Run addSimpleMovingAvg() method to add them first. ")
            
        if ema == True: 
            try: 
                ema = go.Scatter(x=self.df.index, y = self.df['EMA'], line=dict(color="rgba(0, 140, 250, 0.75)", width=1), name="EMA")
                fig.add_trace(ema)
            except: 
                raise Exception("Run addSimpleMovingAvg() method to add them first. ")

        if bollinger == True: 
            try: 
                upper_line = go.Scatter(x=self.df.index, y = self.df['Upper_Bollinger'], line=dict(color="rgba(250, 0, 0, 0.75)", width=1), name="Upper Band")
                
                mid_line = go.Scatter(x=self.df.index, y = self.df['Middle_Bollinger'], line=dict(color="rgba(0, 0, 250, 0.75)", width=0.7), name="Middle Band")
                
                lower_line = go.Scatter(x=self.df.index, y = self.df['Lower_Bollinger'], line=dict(color="rgba(0, 250, 0, 0.75)", width=1), name="Lower Band")  
                
                fig.add_trace(upper_line) 
                fig.add_trace(mid_line) 
                fig.add_trace(lower_line)
                
            except: 
                raise Exception("Run addBollingerBands() method to add them first. ")
            
        if ichimoku == True: 
            
            try: 
                baseline = go.Scatter(x=self.df.index, y = self.df["Baseline"], line=dict(color='pink', width=1), name='Baseline')

                conversion = go.Scatter(x=self.df.index, y = self.df["Conversion"], line=dict(color='black', width=1), name='Conversion')
                
                lagging = go.Scatter(x=self.df.index, y = self.df["Lagging"], line=dict(color='purple', width=1), name='Lagging')
                
                span_a = go.Scatter(x=self.df.index, y = self.df["SpanA"], line=dict(color='green', width=2, dash='dot'), name='Span A')
                
                span_b = go.Scatter(x=self.df.index, y = self.df["SpanB"], line=dict(color='red', width=1, dash='dot'), name='Span B')
                
                fig.add_trace(baseline)
                fig.add_trace(conversion)
                fig.add_trace(lagging)
                fig.add_trace(span_a)
                fig.add_trace(span_b)
                
                def get_fill_color(label): 
                    if label >= 1: 
                        return 'rgba(0, 250, 0, 0.4)' 
                    else: 
                        return 'rgba(250, 0, 0, 0.4)' 
            
                df1 = self.df.copy() 
                df1['label'] = np.where(df1['SpanA'] > df1['SpanB'], 1, 0) 
                df1['group'] = df1['label'].ne(df1['label'].shift()).cumsum() 
                df1 = df1.groupby('group')

                
                dfs = [] 
                for name, data in df1: 
                    dfs.append(data) 
                    
                for df in dfs: 
                    fig.add_traces(go.Scatter(x=df.index, y=df.SpanA, line=dict(color='rgba(0, 0, 0, 0)')))
                    
                    fig.add_traces(go.Scatter(x=df.index, y=df.SpanB, line=dict(color='rgba(0, 0, 0, 0)'), 
                    fill='tonexty', 
                    fillcolor=get_fill_color(df['label'].iloc[0])))
                
                
            except: 
                raise Exception("Run addIchimoku() method to add them first. ")
            
            
        
        fig.update_xaxes(title="Date", 
                         rangeslider_visible=True) 
        fig.update_yaxes(title="Price") 
        
        fig.update_layout(title=f"{self.ticker} Price Data", 
                          height=800, 
                          width=1200, 
                          showlegend=True) 
        fig.show() 