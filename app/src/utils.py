import numpy as np
from scipy.stats import norm
import datetime
import yfinance as yf
import datetime
import requests
import streamlit as st


class Page(object):
    def __init__(self, state):
        self.state = state

    def write(self):
        raise NotImplementedError("Subclass must implement abstract method")


class BlackScholes(object):

    def __init__(self, S, K, t, sigma, r, delta):
        print(t)

        self.S = S
        self.K = K
        self.t = t
        self.sigma = sigma
        self.r = r
        self.delta = delta

    def d1(self):
        numerator = np.log(self.S / self.K) + (self.r - self.delta + 0.5 * (self.sigma ** 2)) * self.t
        denominator = self.sigma * np.sqrt(self.t)
        return numerator / denominator

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.t)

    def call_price(self):
        return (self.S * np.exp(-self.delta * self.t) * norm.cdf(self.d1()) -
                self.K * np.exp(-self.r * self.t) * norm.cdf(self.d2()))

    def put_price(self):
        return (self.K * np.exp(-self.r * self.t) * norm.cdf(-self.d2()) -
                self.S * np.exp(-self.delta * self.t) * norm.cdf(-self.d1()))


def get_parameters(ticker, maturity_date: datetime.date):
    """
        Returns all the necessary parameters for the Black Schols method.

        :param ticker: str: The ticker symbol.
        :param maturity_date: str: The maturity date in the format "YYYY-MM-DD".

        """
    stock = yf.Ticker(ticker)
    stock_prices = stock.history(period="1d")['Close']
    if stock_prices.empty:
        raise ValueError("No stock data available for today.")
    stock_price = stock_prices.iloc[-1]

    historical_data = stock.history(period="1y")['Close']
    daily_returns = historical_data.pct_change().dropna()
    volatility_year = (daily_returns.std() * np.sqrt(252))

    historical_data_30d = stock.history(period="1mo")['Close']
    daily_returns_30d = historical_data_30d.pct_change().dropna()
    volatility_30_day = daily_returns_30d.std() * np.sqrt(252)

    api_key = 'b4a755c93be4ea4a61f4605b9feb0a45'
    series_id = 'IRLTLT01DEM156N'

    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json'
    response = requests.get(url)
    data = response.json()

    if 'observations' not in data or len(data['observations']) == 0:
        raise ValueError("No risk-free rate data available.")

    risk_free_rate = float(data['observations'][-1]['value']) / 100

    days_to_maturity = (maturity_date - datetime.date.today()).days
    years_to_maturity = days_to_maturity / 365

    try:
        dividend_yield = stock.info['dividendYield']
    except KeyError:
        dividend_yield = 0

    return {
        'S': stock_price,
        'volatility_year': volatility_year,
        'volatility_30_Day': volatility_30_day,
        'r': risk_free_rate,
        't': years_to_maturity,
        'delta': dividend_yield
    }

def check_ticker(symbol):
    try:
        stock = yf.Ticker(symbol).info
        if not stock or stock.get("trailingPegRatio") is None:
            return False
        return True
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return False
