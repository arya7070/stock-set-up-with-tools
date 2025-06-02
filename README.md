# stock-set-up-with-tools
📊 Stock Analysis Tools
This Python project provides a suite of tools to:

Scan for inside bar (IB) candle setups in historical stock data.

Open StockCharts RRG and TradingView charts in Chrome for fast technical analysis.

Calculate daily and weekly Average True Range (ATR) for better context on volatility.

Score candles based on a variety of bullish signals, such as no-wick green candles and inside bar setups.

🚀 Features
✅ Fetch historical daily and weekly price data from the Tradier API
✅ Identify inside bar patterns and bullish candle setups
✅ Calculate ATR to contextualize candle movements
✅ Score candles using a flexible set of technical rules
✅ Open StockCharts RRG pages in bulk for relative rotation analysis
✅ Launch TradingView charts in new tabs with one click
✅ Quickly identify potential breakout setups

🔧 Dependencies
Python 3.x

requests

pandas

numpy

matplotlib

How It Works
🔎 Inside Bar Detection: The script uses daily and weekly candle data to spot IBs — periods of consolidation that often precede breakouts.
💚 Bullish Candle Scoring: Combines green candles, no-wick candles, and IBs to score candles and highlight potential momentum.
🌐 RRG Charts: Generate StockCharts RRG links to visualize relative strength.
📊 TradingView: Open multiple TradingView charts in one go for quick chart analysis.

⚠️ Disclaimer
This tool is for educational purposes only and does not provide financial advice. Use at your own risk.
