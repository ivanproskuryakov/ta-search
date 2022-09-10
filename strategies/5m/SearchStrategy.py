import sys
import pandas as pd
import freqtrade.vendor.qtpylib.indicators as qtpylib

from freqtrade.strategy.interface import IStrategy
from search5m import Search5m


class SearchStrategy(IStrategy):
    search5m: Search5m
    minimal_roi = {
        "0": 0.1
    }
    stoploss = -0.05
    n: int
    p: float

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search5m = Search5m(n=self.n, p=self.p)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = self.search5m.find_peaks(df)

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy'] == 'buy'), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['sell'] == 'sell'), 'sell'] = 1

        return df
