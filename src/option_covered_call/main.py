import pandas as pd
from datetime import date, timedelta
from pull_and_plot_covered_call_price import get_call_and_stock_close_price, plot_covered_call_price

tickers = ['TMP','META','AMD','TMP','MSFT','PLTR','GLD','INTC','AMZN','TMP'] #['META','AMD','MSFT','PLTR','GLD','INTC','AMZN']
option_expiration_date = 'May 3, 2024'

today = date.today()
stock_end_date = today + timedelta(3)
stock_start_date = today - timedelta(5)

for ticker in tickers:
    try:
        data = get_call_and_stock_close_price(ticker,option_expiration_date,stock_start_date,stock_end_date)
    except:
        print('=' * 100)
        print(f'{ticker} may not be valid. Please verify and try again!')
        continue
        
    print('=' * 100)
    print(ticker)
    print(data)
    plot_covered_call_price(data,ticker)
    
print('=' * 100)
print('Covered call price data pull and plot completed successfully. Happy trading! :)')

