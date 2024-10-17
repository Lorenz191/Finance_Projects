import streamlit as st
from ..utils import Page, BlackScholes, get_parameters
import datetime
import requests
import numpy as np
import pandas as pd
import yfinance as yf



class Page1(Page):
    def write(self):
        st.title(":blue[Option Price Calculator]")
        st.write(
            "This app calculates the price of European call or put options using the Black Scholes formula."
        )

        # Select exchange (Currently just NYSE as a placeholder)
        exchange = st.selectbox("Select the exchange:", ["NYSE"])

        # Ticker input
        selected_ticker = st.text_input("Enter the ticker symbol of the stock:", placeholder="AAPL")

        # Check for valid ticker symbol
        if selected_ticker:
            try:
                stock_info = yf.Ticker(selected_ticker).info
                if stock_info.get("trailingPegRatio") is None:
                    st.error("Invalid ticker symbol. Please try again.")
                else:
                    st.success("Valid ticker symbol.")

                    # Option parameters
                    with st.expander("Option Parameters"):
                        st.write("Enter the option parameters:")
                        input_date = st.date_input("Maturity date", min_value=datetime.date.today())

                        params = get_parameters(selected_ticker, input_date)
                        t = params['t']
                        S = st.number_input(
                            "Last closing stock price ($)",
                            value=params['S'], disabled=True
                        )
                        K = st.number_input("Strike price ($)")
                        st.write("Select the timespan for the volatility:")
                        period = st.radio("Volatility timespan", ["1y", "1mo"])

                        sigma = params['volatility_year'] if period == "1y" else params['volatility_30_Day']
                        sigma = st.number_input("Volatility (%)",  value=sigma*100, format="%.17f")/100
                        r = st.number_input("Risk-free rate (%)", value=params['r']*100)/100
                        delta = st.number_input("Dividend yield (%)", value=params['delta']*100, format="%.4f", disabled=True)/100 if params[
                            'delta'] else 0


                        st.write(f"The price of a European call option is: :blue[${BlackScholes(S, K, t, sigma, r, delta).call_price():.2f}]")
                        st.write(f"The price of a European put option is: :blue[${BlackScholes(S, K, t, sigma, r, delta).put_price():.2f}]")

            except Exception as e:
                st.error(f"An error occurred: {e}")