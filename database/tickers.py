from pytickersymbols import PyTickerSymbols
from ib_insync import Stock 

large_cap = ["AAPL", "MSFT", "TSLA", "IBM", "AMZN", "META"]

stock_data = PyTickerSymbols()
dax_google = stock_data.get_dax_frankfurt_google_tickers()
dax_yahoo = stock_data.get_dax_frankfurt_yahoo_tickers()
sp100_yahoo = stock_data.get_sp_100_nyc_yahoo_tickers()
sp500_google = stock_data.get_sp_500_nyc_google_tickers()
dow_yahoo = stock_data.get_dow_jones_nyc_yahoo_tickers()