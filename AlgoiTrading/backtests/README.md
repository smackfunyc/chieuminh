# 🧪 RSI + LSMA Guppy Backtest Strategy

A Python-based backtesting framework using the [Backtesting.py](https://kernc.github.io/backtesting.py/) library to simulate a dual-indicator strategy combining **RSI momentum** with a **Linear Regression Moving Average (LSMA)** trend filter.

Built for testing intraday strategies on high-frequency crypto/forex datasets.

---

## 🧠 Strategy Overview

This strategy executes **long or short positions** when:

- RSI is rising or falling (momentum filter)
- Price crosses the LSMA trend line (trend confirmation)
- Minimum risk/reward and stop distance thresholds are met

Exits occur when price closes against the trend.

---

## 📊 Demo

Backtest output and plots are generated on run:

```bash
python rsi_guppy_backtest.py

##  Sample results

| Stat         | Value   |
| ------------ | ------- |
| Total Return | ✅ \~X%  |
| Trades Taken | 📉 \~N  |
| Win Rate     | 🟢 \~Y% |

⚙️ Features

RSI + LSMA indicator fusion
Long/short entries with take profit & stop loss logic
Adaptive SL/TP distance based on market conditions
Simple risk management (2:1 reward:risk ratio)
Candle-level trade execution with position reversal support
🛠 Tech Stack

Python 3.10+
pandas – data manipulation
numpy – numerical ops
TA-Lib – RSI indicator
Backtesting.py – simulation engine
🔐 Requirements

To run this strategy, you'll need:

✅ A historical OHLCV dataset (CSV)
✅ Python environment with required packages
✅ TA-Lib installed (can be tricky on Windows)
Install dependencies:

##Setup Example
data = pd.read_csv("path/to/your_data.csv")
data.index = pd.to_datetime(data['Date'])
data = data[['Open','High','Low','Close','Volume']]

🙏 Credits

Modified by Chieu Minh Nguyen, orignal by https://www.github.com/moondevonyt
Indicators adapted and customized using standard trading logic.

