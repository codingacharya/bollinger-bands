import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
#  USER SETTINGS
# -----------------------------
TICKER = "tcs.ns"          # Change to any symbol: NIFTY.NS, BANKNIFTY.NS, TSLA, BTC-USD, etc.
INTERVAL = "1m"          # 1m, 5m, 15m, 1h, 1d
WINDOW = 20              # Bollinger window
REFRESH = 30             # refresh every 30 seconds
# -----------------------------

plt.style.use("ggplot")

fig, ax = plt.subplots(figsize=(12,6))

def fetch_data():
    data = yf.download(TICKER, period="1d", interval=INTERVAL)
    data["SMA"] = data["Close"].rolling(WINDOW).mean()
    data["STD"] = data["Close"].rolling(WINDOW).std()
    data["Upper"] = data["SMA"] + 2 * data["STD"]
    data["Lower"] = data["SMA"] - 2 * data["STD"]
    return data

def animate(i):
    ax.clear()
    df = fetch_data()

    ax.plot(df.index, df["Close"], label="Close", linewidth=1.5)
    ax.plot(df.index, df["SMA"], label=f"SMA {WINDOW}", linestyle="--")
    ax.plot(df.index, df["Upper"], label="Upper Band")
    ax.plot(df.index, df["Lower"], label="Lower Band")

    ax.fill_between(df.index, df["Upper"], df["Lower"], alpha=0.15)

    ax.set_title(f"Real-Time Bollinger Bands for {TICKER} ({INTERVAL})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")

ani = FuncAnimation(fig, animate, interval=REFRESH * 1000)

plt.tight_layout()
plt.show()
