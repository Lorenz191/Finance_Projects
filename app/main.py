import streamlit as st
from src.pages import PAGE_MAP


def main(state=None):
    current_page = st.sidebar.radio("Go To", list(PAGE_MAP))
    PAGE_MAP[current_page]("active").write()

if __name__ == "__main__":
    main()