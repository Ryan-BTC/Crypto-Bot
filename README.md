# 🧠 Real-Time Crypto Trading Bot (SuperTrend Strategy)
A real-time cryptocurrency trading bot built with Python, utilizing Binance's WebSocket API for low-latency market data and automated trade execution based on the SuperTrend indicator strategy.

## 🚀 Features
**Live Price Streaming:** Connects to Binance via WebSockets for real-time candlestick and trade data.

**SuperTrend Strategy:** Implements the SuperTrend technical indicator to identify trend direction and generate buy/sell signals.

**Live Trade Execution:** Submits market orders directly to Binance via the official API.

**Extensible Design:** Strategy logic and trading parameters are modular and configurable.

### 📦 Tech Stack
Python
Binance WebSocket API via python-binance
WebSockets for real-time market data
Pandas for data manipulation

### ⚙️ Setup
Configure your Binance API keys and settings in config.py.

### 📈 Strategy: SuperTrend
The bot uses the SuperTrend indicator, which relies on ATR (Average True Range) and price action to determine market trends:

**Buy Signal:** When price crosses above the SuperTrend line and enters an uptrend.

**Sell Signal:** When price falls below the SuperTrend line and enters a downtrend.

### ✅ Running the Bot
<pre>python bot.py</pre>

# 🔒 Disclaimer
This project is intended for educational and testing purposes only. Use it at your own risk. Cryptocurrency trading involves significant financial risk — never trade funds you cannot afford to lose.