import pandas as pd
import yfinance as yf

def clean_df(df):
    df[['price', 'value']] = df[['price', 'value']].replace({'\$': '', ',': ''}, regex=True)
    df['shares_change_pct'] = df['shares_change_pct'].replace({'%': '', '\+': '', 'New': '-1', '>999': '-1'}, regex=True)
    df['ticker'] = df['ticker'].str.replace('.', '', regex=False)

    df['price'] = df['price'].astype(float)
    df['value'] = df['value'].astype(float)
    df['shares_change_pct'] = df['shares_change_pct'].astype(float) * 0.01
    return df

def get_sector(ticker):
    try:
        sector = yf.Ticker(ticker).info['sector']
        return sector
    except:
        print('Invalid ticker', ticker, "- Putting 'Unknown' for sector name")
        return 'Unknown'