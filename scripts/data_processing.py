import yfinance as yf
import pandas as pd
from datetime import datetime 
import os
from data_functions import clean_df, get_sector

start_time = datetime.now() 

# speeds up computational time by checking local set instead of fetching yfinance each time
deprecated_tickers = set()

# overwrite existing get_sector function
def get_sector(ticker):
    if ticker in deprecated_tickers:
        return 'Unknown' 
    try:
        sector = yf.Ticker(ticker).info['sector']
        return sector
    except:
        print('Invalid ticker', ticker, "- Putting 'Unknown' for sector name")
        deprecated_tickers.add(ticker)
        return 'Unknown'
    
start_year = datetime(2014,1,1).year 
end_year = datetime.now().year 

trade_type = ['sales', 'buys']

filepath = '../data'

all_df = pd.DataFrame()

for t in trade_type:
    for year in range(start_year, end_year + 1):
        df = pd.read_csv(os.path.join(filepath, f"insider_{t}_{year}.csv"))
        df = clean_df(df)
        df['sector'] = df['ticker'].apply(lambda ticker: get_sector(ticker))
        all_df = pd.concat([df, all_df])

# master datafile with all transactions
all_df.to_csv(os.path.join(filepath, f'insider_master.csv'), index=False)
        
endtime = f"Execution Time: {datetime.now() - start_time}"
print()
print(f'Data cleaned and master csv file saved.')
print(endtime)