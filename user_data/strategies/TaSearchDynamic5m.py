import pandas as pd

from datetime import datetime
from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

from .TaSearchDynamic import TaSearchDynamic


class TaSearchDynamic5m(IStrategy):
    search: TaSearchDynamic

    n: int = 72
    minimal_roi = {
        "0": 0.02,
        "100": 0.01,
        "200": 0.005,
    }
    stoploss = -0.02
    timeframe = '5m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearchDynamic(n=self.n)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        df = self.search.find_extremes(df)
        df = self.buy_volume(df)
        df = self.buy_past_rsi(df)
        df = self.buy_stride(df)

        return df

    def buy_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            df['volume_mean'].loc[i] = round(df[i - self.n:i]['volume'].mean(), 0)

            for x in range(i - 10, i):
                candles = 0

                if x > 1 and df.loc[x]['volume'] > df.loc[i]['volume_mean'] * 2:
                    candles += 1

                    df['buy_volume'].loc[x] = candles
        return df


    def buy_past_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            df['percentage'].loc[i] = self.search.percentage(df[i - self.n:i - 12])

            if df.loc[i]['ex_min_percentage'] and \
                    df.loc[i]['buy_volume'] > -1 and \
                    df.loc[i]['ex_min_percentage'] < -df.loc[i]['percentage']:

                candles = 0

                for x in range(i - 48, i):
                    if x > 1 and df.loc[x]['rsi_7'] < 25:
                        candles += 1

                        df['buy_past_rsi'].loc[x] = candles
                        df['buy_past_rsi'].loc[i] = candles

        return df

    def buy_stride(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            if 20 < df.loc[i]['rsi_7'] < 50:

                for x in range(i - 24, i):
                    if x > 1 \
                            and df.loc[x]['ex_min_percentage'] \
                            and df.loc[x]['buy_volume'] > -1 \
                            and df.loc[x]['ex_min_percentage'] < -df.loc[x]['percentage']:
                        candles = i - x

                        df['buy_stride'].loc[i] = candles
                        df['buy_past_rsi'].loc[i] = df.loc[x]['buy_past_rsi']

                        df['market'].loc[i] = self.search.market(df=df, n=i)
        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['buy_stride'] > -1) & (df['buy_stride'] < 10) &
            (df['buy_past_rsi'] > -1) &
            (df['market'] == -1)
            ,
            'buy'
        ] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] > 75) |
            (df['rsi_30'] > 60),
            'sell'
        ] = 1

        return df

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:

        profit = trade.calc_profit_ratio(rate)

        if exit_reason == 'exit_signal' and profit < 0:
            return False

        return True
