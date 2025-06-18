



import pandas as pd
import backtesting as bt
from backtesting import Backtest, Strategy
from ta.momentum import StochRSIIndicator
import dshare as d
import ccxt

import pandas_ta as ta
import warnings
from backtesting.lib import crossover
#fiilter all warnings
warnings.filterwarnings('ignore')

factor = 1000

class Strat(Strategy):
    rsi_window = 14
    stochrsi_smooth1 = 3
    stochrsi_smooth2 = 3
    bbands_length = 20
    stochrsi_length =14
    bbands_std = 2

    def init(self):
        self.bbands = self.I(bands, self.data)
        self.stoch_rsi_k = self.I(stoch_rsi_k, self.data)
        self.stoch_rsi_d = self.I(stoch_rsi_d, self.data)
        self.buy_price = 0

    def next(self):
        lower = self.bbands[0] #lower BBand
        mid = self.bbands[1] #middle bband
        upper = self.bbands[2] #upper bband

        #check for entry long positions

        if (
            self.data.Close[-1] > lower [-1]  #most recent close is[-1] 

            and crossover(self.stoch_rsi_k, self.stoch_rsi_d)
            
        ):
            self.buy(size =0.05, sl=self.data.Close[-1] * .85, tp = self.data.Close[-1] * 1.40)
            self.buy_price = self.data.Close[-1]

            #get data from discord


def fetch_data(symbol, timeframe, limit=2000):
    exchange = ccxt.phemex({
        'apiKey': d.phemex_key,
        'enableRateLimit': True,
    })

    since = exchange.milliseconds() - (limit *60*60*1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 'ms')
    df.set_index('timestamp', inplace=True)
    #upper case column names
    #df.columns = [x.upper() for x in df.columns]
    df.columns =['Open','High','Low','Close','Volume']
    return df

def bands(data):
    bbands = ta.bbands(close=data.Close.s, length=20, std=2)
    return bbands.to_numpy().T
                
def stoch_rsi_k(data):
    stochrsi = ta.stochrsi(close=data.Close.s, k=3, d=3)
    return stochrsi['STOCHRSIk_14_14_3_3'].to_numpy()
    
def stoch_rsi_d(data):
    stochrsi = ta.stochrsi(close=data.Close.s, k=3, d=3)
    return stochrsi['STOCHRSId_14_14_3_3'].to_numpy()
                
data_df = fetch_data('ETH/USDT', '1h')  # Corrected the symbol format
if not data_df.empty:
    data_df.Open /= factor
    data_df.High /= factor
    data_df.Low /= factor
    data_df.Close /= factor
    data_df.Volume *= factor

    print(data_df.tail())
    
    bt = Backtest(data_df, Strat, cash=1000, commission=0.002)
    stats = bt.run()
    bt.plot()
    print(stats)
else:
    print("The fetched DataFrame is empty, cannot proceed with backtesting.")