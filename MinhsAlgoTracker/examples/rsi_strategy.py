#!/usr/bin/env python3
"""
RSI (Relative Strength Index) Mean Reversion Strategy
This strategy buys when RSI is oversold (<30) and sells when overbought (>70)
"""

import os
import json
import time
import yfinance as yf
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSIStrategy:
    def __init__(self):
        # Get environment variables
        self.script_id = os.environ.get('SCRIPT_ID', '1')
        self.indicator_type = os.environ.get('INDICATOR_TYPE', 'rsi')
        self.indicator_params = json.loads(os.environ.get('INDICATOR_PARAMS', '{"period": 14}'))
        
        # Strategy parameters
        self.symbol = 'AAPL'  # Default symbol
        self.rsi_period = self.indicator_params.get('period', 14)
        self.oversold_level = 30
        self.overbought_level = 70
        self.position = 0  # 0 = no position, 1 = long
        self.balance = 10000  # Starting balance
        self.shares = 0
        
        logger.info(f"RSI Strategy initialized - Period: {self.rsi_period}, Oversold: {self.oversold_level}, Overbought: {self.overbought_level}")
    
    def fetch_data(self, symbol='AAPL', period='5d', interval='1h'):
        """Fetch historical data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def calculate_rsi(self, data):
        """Calculate RSI using TA-Lib"""
        try:
            rsi = talib.RSI(data['Close'].values, timeperiod=self.rsi_period)
            return pd.Series(rsi, index=data.index)
        except:
            # Fallback manual RSI calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
    
    def generate_signals(self, data):
        """Generate buy/sell signals based on RSI levels"""
        rsi = self.calculate_rsi(data)
        
        # Create signals DataFrame
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['rsi'] = rsi
        signals['signal'] = 0.0
        
        # Generate trading signals
        # Buy when RSI < oversold_level
        signals.loc[signals['rsi'] < self.oversold_level, 'signal'] = 1.0
        # Sell when RSI > overbought_level
        signals.loc[signals['rsi'] > self.overbought_level, 'signal'] = -1.0
        
        return signals
    
    def execute_trade(self, signal, price, rsi_value, timestamp):
        """Execute a trade based on the signal"""
        if signal > 0 and self.position == 0:  # Buy signal (RSI oversold)
            if self.balance > 0:
                self.shares = self.balance / price
                self.balance = 0
                self.position = 1
                logger.info(f"BUY: {self.shares:.2f} shares at ${price:.2f} (RSI: {rsi_value:.2f}) on {timestamp}")
                return 'buy'
                
        elif signal < 0 and self.position == 1:  # Sell signal (RSI overbought)
            if self.shares > 0:
                self.balance = self.shares * price
                self.shares = 0
                self.position = 0
                logger.info(f"SELL: {self.shares:.2f} shares at ${price:.2f} (RSI: {rsi_value:.2f}) on {timestamp}")
                return 'sell'
        
        return None
    
    def calculate_portfolio_value(self, current_price):
        """Calculate current portfolio value"""
        return self.balance + (self.shares * current_price)
    
    def run_strategy(self):
        """Main strategy execution loop"""
        logger.info("Starting RSI Mean Reversion Strategy...")
        
        try:
            while True:
                # Fetch latest data
                data = self.fetch_data(self.symbol, period='2d', interval='5m')
                
                if data is None or len(data) < self.rsi_period + 10:
                    logger.warning("Insufficient data, waiting...")
                    time.sleep(60)
                    continue
                
                # Generate signals
                signals = self.generate_signals(data)
                
                # Get latest values
                latest_signal = signals['signal'].iloc[-1]
                latest_price = signals['price'].iloc[-1]
                latest_rsi = signals['rsi'].iloc[-1]
                latest_timestamp = data.index[-1]
                
                # Execute trade if signal present
                if not pd.isna(latest_signal) and latest_signal != 0:
                    trade_type = self.execute_trade(latest_signal, latest_price, latest_rsi, latest_timestamp)
                    
                    if trade_type:
                        portfolio_value = self.calculate_portfolio_value(latest_price)
                        logger.info(f"Portfolio Value: ${portfolio_value:.2f}")
                
                # Log current status
                current_value = self.calculate_portfolio_value(latest_price)
                pnl = current_value - 10000
                
                # Determine RSI status
                rsi_status = "NEUTRAL"
                if latest_rsi < self.oversold_level:
                    rsi_status = "OVERSOLD"
                elif latest_rsi > self.overbought_level:
                    rsi_status = "OVERBOUGHT"
                
                logger.info(f"Price: ${latest_price:.2f}, RSI: {latest_rsi:.2f} ({rsi_status}), Portfolio: ${current_value:.2f}, P&L: ${pnl:.2f}")
                
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
                logger.info(f"Position: {'LONG' if self.position == 1 else 'CASH'}")
                logger.info(f"Shares: {self.shares:.2f}")
                logger.info(f"Cash: ${self.balance:.2f}")

if __name__ == "__main__":
    strategy = RSIStrategy()
    strategy.run_strategy()