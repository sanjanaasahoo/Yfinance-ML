import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- App Title ---
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title("📊 Stock Analysis Dashboard")

# --- Sidebar for Inputs ---
st.sidebar.header("User Input")

# Select Tickers
tickers = st.sidebar.multiselect(
    "Select Companies (tickers):",
    options=["MSFT", "AAPL", "TSLA", "GOOGL", "AMZN", "NVDA"],
    default=["MSFT", "AAPL"]
)

# Date Range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# --- Fetch Data ---
if tickers:
    data = yf.download(tickers, start=start_date, end=end_date)

    # --- Line Chart of Closing Prices ---
    st.subheader("📈 Closing Prices")
    st.line_chart(data["Close"])

    # --- Company Info Section ---
    st.subheader("🏢 Company Information")
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        st.markdown(f"### {ticker}")
        st.json({
            "Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A")
        })

    # --- Balance Sheet Download ---
    st.subheader("📑 Balance Sheet Export")
    selected_ticker = st.selectbox("Choose a company to download balance sheet:", tickers)
    stock = yf.Ticker(selected_ticker)
    balance_sheet = stock.balance_sheet

    if st.button("Download Balance Sheet as CSV"):
        balance_sheet.to_csv(f"{selected_ticker}_Balance_Sheet.csv")
        st.success(f"{selected_ticker}_Balance_Sheet.csv saved!")

    # --- Dividend Data ---
    st.subheader("💰 Dividends")
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        div = stock.dividends
        if not div.empty:
            st.markdown(f"### {ticker} Dividends")
            st.line_chart(div)
        else:
            st.warning(f"{ticker} has no dividend data available.")

else:
    st.warning("Please select at least one company.")
