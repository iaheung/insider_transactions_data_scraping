import pandas as pd
from datetime import datetime, timedelta
import requests
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

start_time = datetime.now() 
end_date = datetime(2014,1,1)

dates_by_year = {}
current_date = start_time

while current_date >= end_date:
    year = current_date.year
    
    if year not in dates_by_year:
        dates_by_year[year] = []
        
    dates_by_year[year].append(current_date)
    current_date = current_date - timedelta(days=1)
    
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

save_dir = '../data'  
if not os.path.exists(save_dir):
        os.mkdir(save_dir)

for year, dates in dates_by_year.items():
    print(f"Saving data from {year}")
    sell_df = pd.DataFrame()
    buy_df = pd.DataFrame()
    for d in dates:
        month = d.strftime('%m')
        day = d.strftime('%d')
        year = d.strftime('%Y')
        
        # selling
        try:
            url = f'''http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={month}%2F{day}%2F{year}+-+{month}%2F{day}%2F{year}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1'''
            response = requests.get(url, headers=headers)
            df = pd.read_html(response.text)

            # only access days where the market was open
            if len(df) == 14:
                df = pd.DataFrame(df[11])
                df.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)
                df.columns = ['transaction_date', 'trade_date', 'ticker', 'company_name', 'owner_name', 'title', 
                                'trade_type', 'price', 'shares_traded', 'shares_after_trade', 'shares_change_pct', 'value']
                
                sell_df = pd.concat([sell_df,df], axis=0)
        except:
            print(f"Error - Could not find date {d}, skipping")
        sell_df.to_csv(os.path.join(save_dir, f'insider_sales_{year}.csv'))
        
        # buying
        try:
            url = f'''http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={month}%2F{day}%2F{year}+-+{month}%2F{day}%2F{year}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1'''
            response = requests.get(url, headers=headers)
            df = pd.read_html(response.text)

            # only access days where the market was open
            if len(df) == 14:
                df = pd.DataFrame(df[11])
                df.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)
                df.columns = ['transaction_date', 'trade_date', 'ticker', 'company_name', 'owner_name', 'title', 
                                'trade_type', 'price', 'shares_traded', 'shares_after_trade', 'shares_change_pct', 'value']
                
                buy_df = pd.concat([buy_df,df], axis=0)
        except:
            print(f"Error - Could not find date {d}, skipping")
        buy_df.to_csv(os.path.join(save_dir, f'insider_buys_{year}.csv'))
    
endtime = f"Execution Time: {datetime.now() - start_time}"
print()
print(f'All CSV Files from {end_date} to {start_time} created.')
print(endtime)