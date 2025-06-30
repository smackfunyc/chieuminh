# 🚀 Algorithmic Trading Platform

A comprehensive web-based algorithmic trading application with real-time charting, backtesting, script management, and multi-exchange API integration.

![Trading Platform](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 **One-Command Setup**

```bash
# Clone the repository
git clone https://github.com/your-username/algo-trading-app.git
cd algo-trading-app

# Install everything (dependencies, environment, etc.)
./install.sh

# Start the platform
./start.sh
```

**That's it! Open http://localhost:3000 in your browser** 🎉

## ✨ Features

### 🎯 Core Functionality
- **Script Upload & Management**: Upload Python/JavaScript trading scripts with configurable parameters
- **Real-Time Dashboard**: Live P&L tracking, portfolio monitoring, and trade execution
- **Technical Indicators**: SMA, EMA, Bollinger Bands, RSI, MACD with real-time visualization
- **Backtesting Engine**: Test strategies on historical data with comprehensive analytics
- **Multi-Exchange Support**: Interactive Brokers, Hyperliquid, Binance, Coinbase Pro, Kraken, Alpaca

### 📊 Advanced Features
- **Real-Time Charting**: Interactive charts with technical indicators
- **Risk Management**: Kill switches, position monitoring, and safety mechanisms
- **API Key Management**: Secure encrypted storage of exchange credentials
- **WebSocket Integration**: Real-time data streaming and updates
- **Portfolio Analytics**: Performance tracking, trade history, and detailed reporting

### 🔒 Security
- **Encrypted API Storage**: All API keys encrypted at rest
- **Secure File Upload**: Validated and sandboxed script execution
- **Authentication Ready**: Framework for user authentication and authorization
- **CORS Protection**: Configured for secure cross-origin requests

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Flask Backend │    │   Data Sources  │
│                 │    │                 │    │                 │
│ • Trading UI    │◄──►│ • REST API      │◄──►│ • Yahoo Finance │
│ • Real-time     │    │ • WebSocket     │    │ • Exchange APIs │
│   Charts        │    │ • Script Engine │    │ • Market Data   │
│ • Backtesting   │    │ • Database      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Docker & Docker Compose** (Recommended)
- **Python 3.11+** (for local development)
- **Node.js 18+** (for local development)
- **TA-Lib** (for technical indicators)

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd algo-trading-app
   ```

2. **Configure environment**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Full Application: http://localhost (via Nginx)

### Option 2: Local Development

1. **Backend Setup**
   ```bash
   cd backend
   
   # Install TA-Lib (macOS)
   brew install ta-lib
   
   # Install TA-Lib (Ubuntu/Debian)
   sudo apt-get install libta-lib-dev
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Run backend
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm start
   ```

## 📖 User Guide

### 1. Initial Setup

1. **Start the Application**
   - Access the web interface at http://localhost:3000
   - Navigate through the tabs: Dashboard, Script Manager, Backtesting, API Keys, Real-Time Chart

2. **Configure API Keys** (Optional for paper trading)
   - Go to "API Keys" tab
   - Select your exchange (Interactive Brokers, Hyperliquid, etc.)
   - Enter your API credentials
   - Test the connection

### 2. Script Management

1. **Upload Trading Scripts**
   - Go to "Script Manager" tab
   - Click "Upload Script"
   - Drag & drop your Python trading script
   - Configure indicator parameters (SMA, EMA, RSI, etc.)
   - Set script name and save

2. **Example Scripts Included**
   - `examples/sma_strategy.py` - Simple Moving Average crossover
   - `examples/rsi_strategy.py` - RSI mean reversion strategy

### 3. Trading Dashboard

1. **Portfolio Management**
   - Set starting balance (default $100)
   - Monitor real-time P&L
   - View active positions and trades

2. **Script Control**
   - Run individual scripts with the play button
   - Stop scripts with the stop button
   - Use "Kill All Scripts" for emergency shutdown

### 4. Backtesting

1. **Configure Backtest**
   - Select symbol (AAPL, GOOGL, BTC-USD, etc.)
   - Choose strategy (SMA, EMA, RSI, Bollinger Bands, MACD)
   - Set date range and initial balance

2. **Analyze Results**
   - View performance metrics
   - Examine trade history
   - Study price charts with signals

### 5. Real-Time Charts

1. **Market Analysis**
   - Enter any symbol (stocks, crypto)
   - Select timeframe (1m, 5m, 1h, 1d)
   - View technical indicators overlay
   - Monitor RSI and volume

2. **Auto-Refresh**
   - Enable auto-refresh for live data
   - Data updates every 30 seconds

## 🔧 Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///trading_app.db

# Interactive Brokers
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=1

# Exchange API Keys
BINANCE_API_KEY=your-api-key
BINANCE_SECRET=your-secret
```

### Trading Script Format

```python
#!/usr/bin/env python3
import os
import json
import yfinance as yf

class TradingStrategy:
    def __init__(self):
        # Get environment variables from platform
        self.script_id = os.environ.get('SCRIPT_ID')
        self.indicator_params = json.loads(os.environ.get('INDICATOR_PARAMS', '{}'))
        
    def run_strategy(self):
        # Your trading logic here
        pass

if __name__ == "__main__":
    strategy = TradingStrategy()
    strategy.run_strategy()
```

## 🛠️ API Documentation

### Script Management
- `GET /api/scripts` - List all scripts
- `POST /api/scripts` - Upload new script
- `POST /api/scripts/{id}/run` - Execute script
- `POST /api/scripts/{id}/stop` - Stop script
- `DELETE /api/scripts/{id}` - Delete script

### Portfolio Management
- `GET /api/portfolio` - Get portfolio data
- `POST /api/portfolio/balance` - Update balance

### Market Data
- `GET /api/market-data/{symbol}` - Get historical data with indicators

### Backtesting
- `POST /api/backtest` - Run backtest with parameters

### API Keys
- `POST /api/api-keys` - Save encrypted API keys

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild services
docker-compose up -d --build

# Scale backend
docker-compose up -d --scale backend=3
```

## 🔒 Security Considerations

### Production Deployment
1. **Change default secrets**
   - Generate strong SECRET_KEY
   - Use environment-specific credentials

2. **Database Security**
   - Use PostgreSQL for production
   - Enable SSL connections
   - Regular backups

3. **API Security**
   - Implement rate limiting
   - Use API authentication
   - Enable HTTPS

4. **Exchange APIs**
   - Use read-only keys for testing
   - Enable IP whitelisting
   - Start with paper trading accounts

### Best Practices
- Never commit API keys to version control
- Use environment variables for secrets
- Regularly rotate API keys
- Monitor account activity
- Implement proper logging

## 📊 Technical Indicators

### Supported Indicators
- **SMA** (Simple Moving Average): Trend following
- **EMA** (Exponential Moving Average): Trend following with more weight on recent prices
- **RSI** (Relative Strength Index): Momentum oscillator (0-100)
- **Bollinger Bands**: Volatility bands around moving average
- **MACD** (Moving Average Convergence Divergence): Trend and momentum

### Usage in Scripts
```python
import talib

# Calculate indicators
sma = talib.SMA(closes, timeperiod=20)
rsi = talib.RSI(closes, timeperiod=14)
upper, middle, lower = talib.BBANDS(closes, timeperiod=20)
```

## 🚨 Troubleshooting

### Common Issues

1. **TA-Lib Installation Failed**
   ```bash
   # macOS
   brew install ta-lib
   
   # Ubuntu/Debian
   sudo apt-get install libta-lib-dev
   
   # Windows
   pip install TA-Lib-0.4.25-cp311-cp311-win_amd64.whl
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   lsof -i :5000
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Docker Issues**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Reset Docker volumes
   docker-compose down -v
   ```

4. **Market Data Issues**
   - Verify internet connection
   - Check symbol format (use Yahoo Finance format)
   - Ensure yfinance is up to date

### Logs and Debugging

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# All service logs
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Use at your own risk.

## 📞 Support

- 📧 Email: support@gmail.com.com
- 💬 Discord: [Join our community](https://discord.gg/algotrading)
- 📖 Documentation: [Full documentation](https://docs.algotrading.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)

## 🎯 Roadmap

- [ ] WebSocket real-time data feeds
- [ ] Machine learning integration
- [ ] Advanced order types
- [ ] Portfolio optimization
- [ ] Paper trading mode
- [ ] Mobile app
- [ ] Advanced risk management
- [ ] Social trading features

---

**Happy Trading! 📈🚀**