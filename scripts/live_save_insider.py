import pandas as pd
from datetime import datetime, timedelta
import requests
import os
import warnings
import sys
warnings.filterwarnings("ignore", category=FutureWarning)

start_time = datetime.now() 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

save_dir = '../data'  
if not os.path.exists(save_dir):
    print("Please run save_insider.py first")
    sys.exit()

print(f"Saving data from {start_time}")

month = start_time.strftime('%m')
day = (start_time - timedelta(1)).strftime('%d')
year = start_time.strftime('%Y')

sell_df = pd.read_csv(os.path.join(save_dir, f'insider_sales_{year}.csv'))
buy_df = pd.read_csv(os.path.join(save_dir, f'insider_buys_{year}.csv'))

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
        
        sell_df = pd.concat([df,sell_df], axis=0)
        sell_df.to_csv(os.path.join(save_dir, f'insider_sales_{year}.csv'), index=False)
except:
    print(f"Error - Could not find date {start_time}")


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
        
        buy_df = pd.concat([df,buy_df], axis=0)
        buy_df.to_csv(os.path.join(save_dir, f'insider_buys_{year}.csv'), index=False)
except:
    print(f"Error - Could not find date {start_time}")

endtime = f"Execution Time: {datetime.now() - start_time}"
print()
print(f'All CSV Files from {start_time} updated.')
print(endtime)