import pandas as pd
from datetime import datetime
import requests
import os

def getSales():
    startTime = datetime.now() 
    url = 'https://www.insidearbitrage.com/insider-sales/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    df = pd.read_html(response.text)

    # list to DataFrame
    df = pd.DataFrame(df[0])

    df.drop(columns=['Unnamed: 1', 'Company', 'Owner', 'Value ($)', 'Filing'], inplace=True, axis=1)

    new_cols = {
        'Symbol': 'ticker',
        'Relationship': 'relation',
        'Date': 'date',
        'Cost': 'share_cost',
        '# Shares': 'num_shares',
        'Total Shares': 'held_shares'
    }

    df.rename(columns=new_cols, inplace=True)

    save_dir = '../data'

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        
    df.to_csv(os.path.join(save_dir, 'data.csv'))

    endtime = f"Execution Time: {datetime.now() - startTime}"
    print()
    print('CSV File: sales.csv created.')
    print(endtime)