def get_call_and_stock_close_price(ticker,option_expiration_date,stock_start_date,stock_end_date):
    """
    Pull option call data and latest stock close price from Yahoo Finance
    """
    
    from yahoo_fin import stock_info as si
    from yahoo_fin import options as op
    import pandas as pd

    stock_data = si.get_data(ticker, start_date=stock_start_date, end_date=stock_end_date)
    stock_close_price = stock_data['close'][-1]
    stock_close_date = stock_data.index[-1].date()
    
    call_data = op.get_calls(ticker, option_expiration_date)[['Strike','Last Price','Bid','Ask','Open Interest']]
    call_data['Expiration Date'] = option_expiration_date
    call_data['Stock Close Price'] = stock_close_price
    call_data['Stock Price +10%'] = stock_close_price * 1.10
    call_data['Stock Close Date'] = stock_close_date
    
    call_data = call_data[(call_data['Strike'] > stock_close_price) & (call_data['Strike'] < stock_close_price*1.20)].reset_index(drop=True)
    
    return call_data


def plot_covered_call_price(df,ticker):
    """
    Plot call option price vs. strike price
    """
    
    import matplotlib.pyplot as plt

    stock_close_price = df['Stock Close Price'][0]
    y_max = df['Ask'].max()
    plt.title(f'{ticker}\nStock Close Price: {stock_close_price:.2f}, +10% Price: {stock_close_price * 1.10:.2f}')
    plt.plot(df['Strike'],df['Bid'],marker='o',label='Bid')
    plt.plot(df['Strike'],df['Ask'],marker='o',label='Ask')
    plt.xlabel('Strike Price ($)')
    plt.ylabel('Bid and Ask Price ($)')
    plt.xlim(left=stock_close_price*0.99)
    plt.ylim(bottom=0)
    plt.axvline(stock_close_price,color='red',linewidth=1)
    plt.text(stock_close_price,y_max*0.1,f'close\n{stock_close_price:.2f}')
    plt.axvline(stock_close_price * 1.10,color='green',linewidth=1)
    plt.text(stock_close_price*1.10,y_max*0.1,f'+10%\n{stock_close_price*1.10:.2f}')
    plt.axvline(stock_close_price * 1.05,color='green',linewidth=1)
    plt.text(stock_close_price*1.05,y_max*0.1,f'+5%\n{stock_close_price*1.05:.2f}')
    plt.grid(color='lightgrey')
    plt.legend()
    plt.show()
