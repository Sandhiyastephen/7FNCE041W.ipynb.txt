# -*- coding: utf-8 -*-
"""7FNCE041W

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17ZzELo_0Qo9Lc-79g_yfqwAkI0G0vOFr
"""

import yfinance as yf
import datetime

# Define the tickers for HSBC and Barclays listed on the LSE
tickers = ["HSBA.L", "BARC.L"]

# Set the date range: from two years ago to today
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=730)  # approximately two years

# Download historical data for both equities with auto_adjust set to False
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)

# Display the first few rows of the 'Adj Close' prices
print("Adjusted Close Prices:")
print(data['Adj Close'].head())

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Define the tickers and date range
tickers = ["HSBA.L", "BARC.L"]
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=730)  # Approximately two years

# Download historical data with auto_adjust disabled so that Adj Close is available
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
adj_close = data['Adj Close']

# Plot the equity prices over time
plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(adj_close[ticker], label=ticker)
plt.title("Price Movements of HSBC and Barclays")
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price")
plt.legend()
plt.show()

# Calculate daily returns
daily_returns = adj_close.pct_change().dropna()

# Annualisation factor for trading days (approx. 252)
trading_days = 252

# Calculate annualised average returns and standard deviations (volatility)
annual_return = daily_returns.mean() * trading_days
annual_volatility = daily_returns.std() * np.sqrt(trading_days)

print("Annualised Average Returns:")
print(annual_return)
print("\nAnnualised Standard Deviations (Volatility):")
print(annual_volatility)

# Calculate daily returns (if not already computed)
daily_returns = adj_close.pct_change().dropna()

# Compute the correlation matrix of daily returns
correlation = daily_returns.corr()
print("Correlation matrix:")
print(correlation)

# Extract the correlation coefficient between HSBC and Barclays
corr_value = correlation.loc["HSBA.L", "BARC.L"]
print("Correlation between HSBC and Barclays:", corr_value)

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np

# Define tickers and date range (last 2 years)
tickers = ["HSBA.L", "BARC.L"]
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=730)

# Download historical data with auto_adjust=False so 'Adj Close' is available
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
adj_close = data['Adj Close']

# Compute daily returns
daily_returns = adj_close.pct_change().dropna()

# Calculate correlation matrix
correlation = daily_returns.corr()

# Plot correlation heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Daily Returns")
plt.show()

# Plot scatter plot to visualize the relationship between the daily returns of the two stocks
plt.figure(figsize=(8,6))
plt.scatter(daily_returns["HSBA.L"], daily_returns["BARC.L"], alpha=0.5, color='green')
plt.title("Scatter Plot of Daily Returns: HSBA.L vs BARC.L")
plt.xlabel("HSBA.L Daily Returns")
plt.ylabel("BARC.L Daily Returns")
plt.grid(True)
plt.show()

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# --- Step 1: Download Historical Data ---
tickers = ["HSBA.L", "BARC.L"]
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=730)  # ~2 years of data

data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)['Adj Close']

# --- Step 2: Define a function to create SMA signals ---
def sma_strategy_signals(prices, short_window=50, long_window=200):
    """
    Returns a DataFrame containing:
    - Price
    - Short SMA
    - Long SMA
    - Trading signals (Buy=1, Sell=-1)
    """
    df = pd.DataFrame(index=prices.index)
    df['Price'] = prices
    df['ShortSMA'] = df['Price'].rolling(window=short_window, min_periods=1).mean()
    df['LongSMA'] = df['Price'].rolling(window=long_window, min_periods=1).mean()

    # Generate signals: 1 = Buy, -1 = Sell, 0 = Hold
    df['Signal'] = 0

    # When short SMA crosses above long SMA => Buy
    df.loc[df['ShortSMA'] > df['LongSMA'], 'Signal'] = 1

    # When short SMA crosses below long SMA => Sell
    df.loc[df['ShortSMA'] < df['LongSMA'], 'Signal'] = -1

    # Identify points of crossover by comparing current Signal to previous Signal
    df['Trade'] = df['Signal'].diff()

    return df

# --- Step 3: Apply the strategy and plot the signals for each equity ---
plt.figure(figsize=(14, 6))

for i, ticker in enumerate(tickers, 1):
    df_signals = sma_strategy_signals(data[ticker])

    # Create a subplot for each ticker
    ax = plt.subplot(1, 2, i)
    ax.plot(df_signals.index, df_signals['Price'], label=f"{ticker} Price", alpha=0.5)
    ax.plot(df_signals.index, df_signals['ShortSMA'], label='Short SMA (50)', color='blue', alpha=0.7)
    ax.plot(df_signals.index, df_signals['LongSMA'], label='Long SMA (200)', color='orange', alpha=0.7)

    # Plot buy signals (where 'Trade' == 2 => from -1 to +1, or from 0 to +1)
    buy_signals = df_signals[df_signals['Trade'] == 2].index.union(
        df_signals[(df_signals['Signal'] == 1) & (df_signals['Signal'].shift(1) == 0)].index
    )
    # Plot sell signals (where 'Trade' == -2 => from +1 to -1, or from 0 to -1)
    sell_signals = df_signals[df_signals['Trade'] == -2].index.union(
        df_signals[(df_signals['Signal'] == -1) & (df_signals['Signal'].shift(1) == 0)].index
    )

    # Annotate buy signals
    ax.scatter(buy_signals, df_signals.loc[buy_signals, 'Price'],
               marker='^', color='green', s=100, label='Buy Signal')
    # Annotate sell signals
    ax.scatter(sell_signals, df_signals.loc[sell_signals, 'Price'],
               marker='v', color='red', s=100, label='Sell Signal')

    ax.set_title(f"SMA Crossover Strategy - {ticker}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

plt.tight_layout()
plt.show()