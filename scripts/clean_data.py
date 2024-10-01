import os
import pandas as pd
from concat_dfs import concatenate_dfs

import warnings
warnings.filterwarnings("ignore")

trades = {
    'buys': concatenate_dfs(2014, 2024, 'buys'),
    'sales': concatenate_dfs(2014, 2024, 'sales')
}

all_insiders = pd.DataFrame()

for key in trades.keys():
    df = trades[key]
    
    df = df[['transaction_date', 'trade_date', 'ticker',
        'company_name', 'owner_name', 'title', 'trade_type', 'price',
        'shares_traded', 'shares_after_trade', 'shares_change_pct', 'value', 'sector']]

    df[['price', 'value']] = df[['price', 'value']].replace({'\$': '', ',': ''}, regex=True)
    df['shares_change_pct'] = df['shares_change_pct'].replace({'%': '', '\+': '', 'New': '-1', '>999': '-1'}, regex=True)
    df['ticker'] = df['ticker'].str.replace('.', '', regex=False)

    df['price'] = df['price'].astype(float)
    df['value'] = df['value'].astype(float)
    df['shares_change_pct'] = df['shares_change_pct'].astype(float) * 0.01

    filepath = '../data'
    df.to_csv(os.path.join(filepath, f'insider_{key}.csv'), index=False)
    
    all_insiders = pd.concat([all_insiders, df])
    
all_insiders.to_csv(os.path.join(filepath, 'insider_all.csv'), index=False)

print("Three files: [insider_buys.csv, insider_sales.csv, insider_all.csv] created")    