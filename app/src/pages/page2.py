from attr.validators import disabled

from ..utils.utils import Page, check_ticker
import streamlit as st

class Page2(Page):

    def write(self):
        st.title(":blue[Monte Carlo]")

        exchange = st.selectbox("Select the exchange:", ["NYSE"])

        selected_ticker = st.text_input("Enter the ticker symbol of the stock:", placeholder="AAPL")

        if selected_ticker:
            if not check_ticker(selected_ticker):
                st.error("Invalid ticker symbol. Please try again.")
            else:
                st.success("Valid ticker symbol.")

