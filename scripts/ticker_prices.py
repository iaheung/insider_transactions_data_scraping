import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

# moving average period
PERIOD = 50
tickersDict = {}

def get_info(ticker, start, end, n):
    try:
        tickerdf = yf.download(ticker, start, end, progress=False)
        # most recent close price 
        current_price = tickerdf['Close'].iloc[-1]
        moving_average = pd.Series(tickerdf["Close"].rolling(n, min_periods=0).mean(),name='moving_average')
        return (current_price, moving_average.iloc[-1])
    except:
        return (None, None)
    
def get_price(x, start, end):
    ticker = x
    if ticker not in tickersDict.keys():
        tick_price, tick_ma = get_info(ticker, start, end, PERIOD)
        tickersDict[ticker] =  {
            'price': tick_price,
            'ma': tick_ma
        }
    return tickersDict[ticker]['price']
    
def get_ma(x, start, end):
    ticker = x
    if ticker not in tickersDict.keys():
        tick_price, tick_ma = get_info(ticker, start, end, PERIOD)
        tickersDict[ticker] =  {
            'price': tick_price,
            'ma': tick_ma
        }
    return tickersDict[ticker]['ma']
        
startTime = datetime.now()

csv_directory = '../data'
 
df = pd.read_csv(os.path.join(csv_directory, 'insider_all.csv'))

unique_tickers = pd.DataFrame({'ticker': df['ticker'].unique()})

# days is number of days of data to collect from yfinance for moveing average computation based on PERIOD
days = PERIOD

# start and end dates for yfinance
start = startTime - timedelta(days)
end = startTime

unique_tickers['current_price'] = unique_tickers['ticker'].apply(lambda x: get_price(x, start, end))
unique_tickers[f'moving_average_{PERIOD}'] = unique_tickers['ticker'].apply(lambda x: get_ma(x, start, end))

unique_tickers.to_csv(os.path.join(csv_directory, 'ticker_price_list.csv'), index=False)

endtime = f"Execution Time: {datetime.now() - startTime}"
print(f'ticker_price_list.py - Stock prices for today at {startTime}, collected')
print(f'Moving average period: {PERIOD}')
print(endtime)