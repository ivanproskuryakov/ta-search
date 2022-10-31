import pandas as pd

from freqtrade.strategy.interface import IStrategy
from user_data.strategies.taSearch import TaSearch


class TaSearch30m(IStrategy):
    search: TaSearch
    n: int
    p: float

    n = 72
    p = 5
    minimal_roi = {
        "0": 0.03
    }
    stoploss = -0.1
    timeframe = '30m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearch(n=self.n, p=self.p)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = self.search.find_extremes(df)

        df = self.buy_past_rsi(df)
        df = self.buy_stride(df)

        return df

    def buy_past_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            if df.loc[i]['ex_min_percentage'] and df.loc[i]['ex_min_percentage'] < -self.p:
                c = 0
                for x in range(i - 48, i):
                    if x > 1 and df.loc[x]['rsi_7'] < 30:
                        c += 1
                        df['buy_past_rsi'].loc[x] = c
                        df['buy_past_rsi'].loc[i] = c

        return df

    def buy_stride(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            if 25 < df.loc[i]['rsi_7'] < 40:
                for x in range(i - 24, i):
                    if x > 1 \
                            and df.loc[x]['ex_min_percentage'] \
                            and df.loc[x]['ex_min_percentage'] < -self.p:
                        df['buy_stride'].loc[i] = i - x
                        df['buy_past_rsi'].loc[i] = df.loc[x]['buy_past_rsi']
        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy_stride'] > 0) & (df['buy_past_rsi'] > 2), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['rsi_7'] > 70), 'sell'] = 1

        return df
