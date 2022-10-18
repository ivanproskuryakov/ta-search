import pandas as pd

from freqtrade.strategy.interface import IStrategy
from taSearch import TaSearch


class TaSearch30m(IStrategy):
    search: TaSearch
    n: int
    p: float

    n = 48
    p = 5
    minimal_roi = {
        "0": 0.03
    }
    stoploss = -0.01
    timeframe = '30m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearch(n=self.n, p=self.p)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = self.search.find_extremes(df)
        df = self.find_buy_entry(df)

        df['sell'] = df.apply(lambda row: self.populate_sell(row), axis=1)

        return df

    def find_buy_entry(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            if 40 > df.loc[i]['rsi_7'] < 50:
                for x in range(i - 4, i):
                    if df.loc[x]['ex_min_percentage'] and df.loc[x]['ex_min_percentage'] < -self.p:
                        df['buy'].loc[i] = 'buy'

        return df

    def populate_sell(self, row: pd.DataFrame):
        if row['rsi_7'] > 70:
            return 'sell'
        else:
            return ''

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy'] == 'buy'), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['sell'] == 'sell'), 'sell'] = 1

        return df
