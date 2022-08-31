import sys
import pandas as pd
import freqtrade.vendor.qtpylib.indicators as qtpylib

from freqtrade.strategy.interface import IStrategy

from search import Search

search = Search()

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


class TaSearch8N72(IStrategy):
    minimal_roi = {
        "0": 0.08
    }
    stoploss = -0.25
    timeframe = '1h'

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = search.find_peaks(df, n=72)

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy'] == 'buy'), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # df.loc[(df['sell'] == 'sell'), 'sell'] = 1

        return df
