from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np
import talib
print("RSI GUppy strategy OG loading....")
class LSMAGuppyRSI(Strategy):
    lsma_period = 55
    rsi_period = 14
    risk_multiplier = 2
    min_stop_distance = .002 #increased to 2% minimum distance
    min_reward_ratio = 1.5 #Minimum reward:risk ratio

    def init(self):
        print('RSI GUPPY Strategy initialization')
        close = self.data.Close
        time_period = np.arange(len(close))
        self.lsma = self.I(lambda x: self.calculate_lsma(x, self.lsma_period), close)
        
        self.rsi = self.I(talib.RSI, close, self.rsi_period)
        print("🍹 Indicators created successfully!")

    def calculate_lsma(self, data, period):
        """Calculate linear regression moving average"""
        print("🧪Calculating LSMA")
        result = np.zeros_like(data)
        for i in range(period-1, len(data)):
            x = np.arange(period)
            y = data[i-period+1:i+1]
            slope, intercept = np.polyfit(x,y,1)
            result[i] = slope * (period -1) + intercept
        return result
    
    #this runs on each bar
    def next(self):
        price = self.data.Close[-1]

        if price <= 0:
            print(f"⚠️Warning: Invalid price detected: {price}")
            return
        is_green_candle = self.data.Close[-1] > self.data.Open[-1]

        #check if RSI is rising
        rsi_rising = self.rsi[-1] > self.rsi[-2]
    
        #check long conditions
        long_conditions = (
            is_green_candle and
            price > self.lsma[-1] and
            rsi_rising
        )

        #check short conditions
        short_conditions = (
            not is_green_candle and
            price < self.lsma[-1] and
            not rsi_rising
        ) 

        #entry signals
        if not self.position:
            if long_conditions:
                #calculate stop loss with minimum distance
                #for longs sl must be below entry price, tp above
                #sl_distance = max(self.min_stop_distance * price, price - self)
                sl_price = min(self.lsma[-1], price * 0.99)
                sl_distance = price - sl_price  
                        
 #               tp_distance = sl_distance * self.risk_multiplier
                tp_price = price + (sl_distance * self.risk_multiplier)

                if sl_price < price < tp_price:
                    self.buy(sl=sl_price, tp=tp_price)
            elif short_conditions:
                # Calculate stop loss minimum distance
                #sl_distance = max(self.min_stop_distance * price, self.lsma[-1])
                sl_price = max(self.lsma[-1], price * 1.01)
                sl_distance = sl_price - price
                #tp_distance = sl_distance * self.risk_multiplier
                tp_price = price - (sl_distance * self.risk_multiplier)

                if tp_price < price < sl_price:
                    self.sell(sl=sl_price, tp=tp_price)
        #exit signals
        if self.position.is_long and price < self.lsma[-1]:
                self.position.close()
        elif self.position.is_short and price > self.lsma[-1]:
                self.position.close()
#load in the data
data = pd.read_csv("/Users/macm4/Desktop/productivity/data/ETHUSD_1m_060124_01012025.csv")

#data: Date,Open,High,Low,Close,Volume
data.index = pd.to_datetime(data['Date'])
data = data[['Open','High','Low','Close','Volume']]  

bt= Backtest(data, LSMAGuppyRSI, cash=100000, commission=0.002, exclusive_orders=True)

print("\n Starting Backtest...")
stats = bt.run()
print(stats)

#print("\n Generating plot...")
bt.plot()
#print(" OG RSI Guppy Strategy complete!") 
