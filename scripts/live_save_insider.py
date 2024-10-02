import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import requests
from data_functions import clean_df, get_sector

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

start_time = datetime.now()
yesterday = start_time - timedelta(1)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

filepath = '../data'  
if not os.path.exists(filepath):
    print("Please run save_insider.py first")
    sys.exit()

print(f"Saving data from {yesterday.date()}")

month = yesterday.strftime('%m')
day = yesterday.strftime('%d')
year = yesterday.strftime('%Y')

buy_df = pd.read_csv(os.path.join(filepath, f'insider_buys_{year}.csv'))

# for url formatting, s - sale, p - purchase (buy)
trade_type = {'sales':'s', 
              'buys': 'p'}

for t in trade_type.keys():
    save_df = pd.read_csv(os.path.join(filepath, f'insider_{t}_{year}.csv'))
    try:
        url = f'''http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={month}%2F{day}%2F{year}+-+{month}%2F{day}%2F{year}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&x{trade_type[t]}=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1'''
        response = requests.get(url, headers=headers)
        df = pd.read_html(response.text)

        # only access days where the market was open
        if len(df) == 14:
            df = pd.DataFrame(df[11])
            df.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)
            df.columns = ['transaction_date', 'trade_date', 'ticker', 'company_name', 'owner_name', 'title', 
                            'trade_type', 'price', 'shares_traded', 'shares_after_trade', 'shares_change_pct', 'value']
            
            save_df = pd.concat([df,save_df], axis=0)
    
            save_df.to_csv(os.path.join(filepath, f'insider_{t}_{year}.csv'), index=False)
            
            # clean data and add sector info for insider_master.csv
            df = clean_df(df)
            df['sector'] = df['ticker'].apply(lambda ticker: get_sector(ticker))

            # updating insider_master.csv with cleaned data
            master_df = pd.read_csv(os.path.join(filepath, 'insider_master.csv'))
            master_df = pd.concat([df, master_df])
            master_df.to_csv(os.path.join(save_df, f'insider_master.csv'), index=False)
    except:
        print(f"Error - Could not find date {yesterday.date()}")
    
endtime = f"Execution Time: {datetime.now() - start_time}"
print()
print(f'All CSV Files from {yesterday.date()} updated.')
print(endtime)