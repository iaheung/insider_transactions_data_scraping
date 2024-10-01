import yfinance as yf

def get_sector(ticker): 
    try:
        sector = yf.Ticker(ticker).info['sector']
        return sector
    except:
        print('Invalid ticker', ticker, "- Putting 'Unknown' for sector name")
        print()
        return 'Unknown'