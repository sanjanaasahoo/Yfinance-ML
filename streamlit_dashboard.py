import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- App Config ---
st.set_page_config(page_title="Stock Financial Analysis", layout="wide")
st.title("📊 Stock Analysis Dashboard")

# --- Sidebar Inputs ---
st.sidebar.header("User Input")

tickers = st.sidebar.multiselect(
    "Select Companies (tickers):",
    options=["MSFT", "AAPL", "TSLA", "GOOGL", "AMZN", "NVDA"],
    default=["MSFT", "AAPL"]
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# --- Cached Functions ---
@st.cache_data
def get_stock_data(tickers, start, end):
    return yf.download(tickers, start=start, end=end)

@st.cache_data
def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info
    except:
        return {}

@st.cache_data
def get_balance_sheet(ticker):
    stock = yf.Ticker(ticker)
    return stock.balance_sheet

@st.cache_data
def get_dividends(ticker):
    stock = yf.Ticker(ticker)
    return stock.dividends

# --- Fetch Data ---
if tickers:

    data = get_stock_data(tickers, start_date, end_date)

    # Closing Prices
    st.subheader("📈 Closing Prices")
    st.line_chart(data["Close"])

    # Company Info
    st.subheader("🏢 Company Information")

    for ticker in tickers:
        info = get_company_info(ticker)

        st.markdown(f"### {ticker}")
        st.json({
            "Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A")
        })

    # Balance Sheet Export
    st.subheader("📑 Balance Sheet Export")

    selected_ticker = st.selectbox(
        "Choose a company to download balance sheet:",
        tickers
    )

    balance_sheet = get_balance_sheet(selected_ticker)

    if st.button("Download Balance Sheet as CSV"):
        balance_sheet.to_csv(f"{selected_ticker}_Balance_Sheet.csv")
        st.success(f"{selected_ticker}_Balance_Sheet.csv saved!")

    # Dividends
    st.subheader("💰 Dividends")

    for ticker in tickers:
        div = get_dividends(ticker)

        if not div.empty:
            st.markdown(f"### {ticker} Dividends")
            st.line_chart(div)
        else:
            st.warning(f"{ticker} has no dividend data available.")

else:
    st.warning("Please select at least one company.")