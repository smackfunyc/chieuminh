#!/usr/bin/env python3
"""
Simple Moving Average (SMA) Crossover Strategy
This is an example trading script that demonstrates SMA crossover logic.
"""

import os
import json
import time
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMAStrategy:
    def __init__(self):
        # Get environment variables
        self.script_id = os.environ.get('SCRIPT_ID', '1')
        self.indicator_type = os.environ.get('INDICATOR_TYPE', 'sma')
        self.indicator_params = json.loads(os.environ.get('INDICATOR_PARAMS', '{"period": 20, "fast": 10, "slow": 20}'))
        
        # Strategy parameters
        self.symbol = 'AAPL'  # Default symbol
        self.fast_period = self.indicator_params.get('fast', 10)
        self.slow_period = self.indicator_params.get('slow', 20)
        self.position = 0  # 0 = no position, 1 = long, -1 = short
        self.balance = 10000  # Starting balance
        self.shares = 0
        
        logger.info(f"SMA Strategy initialized - Fast: {self.fast_period}, Slow: {self.slow_period}")
    
    def fetch_data(self, symbol='AAPL', period='5d', interval='1h'):
        """Fetch historical data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def calculate_sma(self, data, period):
        """Calculate Simple Moving Average"""
        return data['Close'].rolling(window=period).mean()
    
    def generate_signals(self, data):
        """Generate buy/sell signals based on SMA crossover"""
        fast_sma = self.calculate_sma(data, self.fast_period)
        slow_sma = self.calculate_sma(data, self.slow_period)
        
        # Create signals
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['fast_sma'] = fast_sma
        signals['slow_sma'] = slow_sma
        signals['signal'] = 0.0
        
        # Generate trading signals
        signals['signal'][self.fast_period:] = np.where(
            signals['fast_sma'][self.fast_period:] > signals['slow_sma'][self.fast_period:], 1.0, 0.0
        )
        
        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        
        return signals
    
    def execute_trade(self, signal, price, timestamp):
        """Execute a trade based on the signal"""
        if signal > 0 and self.position <= 0:  # Buy signal
            if self.balance > 0:
                self.shares = self.balance / price
                self.balance = 0
                self.position = 1
                logger.info(f"BUY: {self.shares:.2f} shares at ${price:.2f} on {timestamp}")
                return 'buy'
                
        elif signal < 0 and self.position >= 0:  # Sell signal
            if self.shares > 0:
                self.balance = self.shares * price
                self.shares = 0
                self.position = 0
                logger.info(f"SELL: {self.shares:.2f} shares at ${price:.2f} on {timestamp}")
                return 'sell'
        
        return None
    
    def calculate_portfolio_value(self, current_price):
        """Calculate current portfolio value"""
        return self.balance + (self.shares * current_price)
    
    def run_strategy(self):
        """Main strategy execution loop"""
        logger.info("Starting SMA Crossover Strategy...")
        
        try:
            while True:
                # Fetch latest data
                data = self.fetch_data(self.symbol, period='1d', interval='5m')
                
                if data is None or len(data) < self.slow_period:
                    logger.warning("Insufficient data, waiting...")
                    time.sleep(60)
                    continue
                
                # Generate signals
                signals = self.generate_signals(data)
                
                # Get latest signal
                latest_signal = signals['positions'].iloc[-1]
                latest_price = signals['price'].iloc[-1]
                latest_timestamp = data.index[-1]
                
                # Execute trade if signal present
                if not pd.isna(latest_signal) and latest_signal != 0:
                    trade_type = self.execute_trade(latest_signal, latest_price, latest_timestamp)
                    
                    if trade_type:
                        portfolio_value = self.calculate_portfolio_value(latest_price)
                        logger.info(f"Portfolio Value: ${portfolio_value:.2f}")
                
                # Log current status
                current_value = self.calculate_portfolio_value(latest_price)
                pnl = current_value - 10000
                logger.info(f"Current Price: ${latest_price:.2f}, Portfolio: ${current_value:.2f}, P&L: ${pnl:.2f}")
                
                # Wait before next iteration
                time.sleep(300)  # 5 minutes
                
        except KeyboardInterrupt:
            logger.info("Strategy stopped by user")
        except Exception as e:
            logger.error(f"Strategy error: {e}")
        finally:
            # Final portfolio summary
            final_data = self.fetch_data(self.symbol, period='1d', interval='1m')
            if final_data is not None:
                final_price = final_data['Close'].iloc[-1]
                final_value = self.calculate_portfolio_value(final_price)
                total_return = ((final_value - 10000) / 10000) * 100
                
                logger.info("=== STRATEGY SUMMARY ===")
                logger.info(f"Initial Balance: $10,000.00")
                logger.info(f"Final Portfolio Value: ${final_value:.2f}")
                logger.info(f"Total Return: {total_return:.2f}%")
                logger.info(f"Position: {self.position}")
                logger.info(f"Shares: {self.shares:.2f}")
                logger.info(f"Cash: ${self.balance:.2f}")

if __name__ == "__main__":
    strategy = SMAStrategy()
    strategy.run_strategy()