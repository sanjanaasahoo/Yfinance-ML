import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

msft = yf.Ticker("MSFT")
print(msft.financials)
print(msft.balancesheet)
print(msft.info)
btc=yf.Ticker("BTC-USD")
print(btc.info["regularMarketPrice"])
data=yf.download(["MSFT","TSLA","AAPL "], start="2020-06-01", end="2021-01-01")
data["Close"].plot(title="Closing Price of 3 MNCs ")
plt.show()

msft_balance = msft.balance_sheet
msft_balance.to_excel("MSFT_Balance_Sheet.xlsx")
aapl=yf.Ticker("AAPL")
aapl_div = aapl.dividends

aapl_div.index = aapl_div.index.tz_localize(None)
aapl_div.to_excel("AAPL_Dividends.xlsx")

