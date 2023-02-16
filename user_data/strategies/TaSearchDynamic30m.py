import pandas as pd

from datetime import datetime
from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

from TaSearchDynamic import TaSearchDynamic


class TaSearchDynamic30m(IStrategy):
    search: TaSearchDynamic

    n: int = 200
    minimal_roi = {
        "0": 0.1,
    }
    stoploss = -0.0
    timeframe = '30m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearchDynamic(n=self.n)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        df = self.search.find_extremes(df)
        df = self.buy_past_rsi(df)
        df = self.buy_stride(df)

        return df

    def buy_past_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df.tail(200).iterrows():
            df['percentage'].loc[i] = self.search.percentage(df[i - self.n:i - 48])

            if df.loc[i]['ex_min_percentage'] and \
                    df.loc[i]['ex_min_percentage'] < -df.loc[i]['percentage']:

                candles = 0

                for x in range(i - 48, i):
                    if x > 1 and df.loc[x]['rsi_7'] < 35:
                        candles += 1

                        df['buy_past_rsi'].loc[x] = candles
                        df['buy_past_rsi'].loc[i] = candles

        return df

    def buy_stride(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df.tail(100).iterrows():
            if 45 < df.loc[i]['rsi_7'] < 75:

                for x in range(i - 72, i):
                    if x > 1 \
                            and df.loc[i]['rsi_7'] > 55 \
                            and df.loc[x]['rsi_7'] < df.loc[i]['rsi_7'] \
                            and df.loc[x]['ex_min_percentage'] \
                            and df.loc[x]['ex_min_percentage'] < -df.loc[x]['percentage']:
                            # and df.loc[i]['volume'] > df.loc[i]['volume_mean'] \
                            # and df.loc[i]['volume_mean'] < df.loc[i - 48]['volume_mean'] * 2 \
                        candles = i - x

                        df['buy_stride'].loc[i] = candles
                        df['buy_past_rsi'].loc[i] = df.loc[x]['buy_past_rsi']

                        df['market'].loc[i] = self.search.market(df=df, n=i)
        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['buy_stride'] > 4) & (df['buy_stride'] < 10) &
            (df['buy_past_rsi'] > 2)
            ,
            'buy'
        ] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] > 85) |
            (df['rsi_30'] > 75),
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
