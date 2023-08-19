import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.environ.get('API_KEY')

headers = {
    'X-MBX-APIKEY': api_key,
}

def ping():
    r = requests.get('https://api.binance.com/api/v3/time')
    return r.content

def get_top5_ticker_prices():
    r = requests.get('https://api.binance.com/api/v3/ticker/price')
    tickers_price = r.json()

    selected_tickers = []
    selected_tickers_json = {}
    for ticker_price in tickers_price:
        if ticker_price.get('symbol').endswith('USDT'):
            selected_tickers.append(ticker_price)
            selected_tickers_json[ticker_price.get('symbol')] = float(ticker_price.get('price'))
        if len(selected_tickers) == 5:
            break

    return selected_tickers, selected_tickers_json
