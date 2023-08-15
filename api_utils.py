import yfinance as yf

def get_current_sp500_price():
    sp500 = yf.Ticker('^GSPC')
    current_price = sp500.history(period='1d')['Close'][-1]
    return current_price