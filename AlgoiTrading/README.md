# 🏦 Interactive Brokers Bracket Order Bot

A fully automated Python script to execute **bracket orders** on the Interactive Brokers (IBKR) platform using their official [IB API](https://interactivebrokers.github.io/).

Built for **quantitative traders** and **algorithmic strategists** who want fast, reproducible order placement with built-in risk management via stop-loss and take-profit logic.

---

## 🔐 Requirements

To use this bot, you’ll need:

- ✅ A funded [Interactive Brokers (IBKR) account](https://www.interactivebrokers.com/)
- ✅ [Trader Workstation (TWS)](https://www.interactivebrokers.com/en/index.php?f=16040) or [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-software.php)
- ✅ IB API enabled via TWS/Gateway settings
- ✅ Python 3.10+ with required packages (see below)

Install Python dependencies with:

```bash
pip install -r requirements.txt

<!--
## 🌐 Live Demo

> 🔗 [Live GitHub Repo](https://github.com/smackfunyc/chieuminh)

> 💻 Demo terminal output available via screenshots below.

---

 ## 📸 Screenshots

| Order Execution | Confirmation |
|-----------------|--------------|
| ![placing](https://user-images.githubusercontent.com/your-demo-1.png) | ![filled](https://user-images.githubusercontent.com/your-demo-2.png) |
-->
---

## ⚙️ Features

- ✅ Connects to IBKR paper or live TWS
- 🔁 Executes bracket orders with:
  - Entry Limit Order
  - Stop Loss
  - Take Profit
- 🧠 Calculates Risk-Reward Ratio
- 🧵 Thread-safe execution using multithreading
- ⏱ Timeout & error handling for robustness

---

## 🛠 Tech Stack

- `Python 3.10+`
- `ib_insync` (IB API) ibapi==9.81.1.post1
- `threading`, `time` – for async order monitoring
- Runs via `TWS` or `IB Gateway` (paper/live mode)

---

## 🚀 Setup Instructions

1. **Install IB API**:
   ```bash
   pip install ibapi

