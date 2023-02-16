import pandas as pd

from datetime import datetime
from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

from TaSearchDynamic import TaSearchDynamic


class TaSearchDynamic5m(IStrategy):
    search: TaSearchDynamic

    n: int = 108
    minimal_roi = {
        "0": 0.05,
        "360": 0.02,
    }
    stoploss = -0.02
    timeframe = '5m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearchDynamic(n=self.n)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

        no_volume = len(df.tail(200).query(f'volume == 0'))

        df = self.search.find_extremes(df)

        if no_volume > 0:
            return df

        df = self.buy_minimum(df)
        df = self.buy_past_rsi(df)
        df = self.buy_stride(df)

        return df

    def buy_minimum(self, df: pd.DataFrame) -> pd.DataFrame:
        i = df.tail(1).index

        min_ext = df.tail(600)['close'].min() * 0.98 # -2% stoploss
        min_last = df.loc[i]['close'].min()

        if min_last < min_ext:
            df['buy_min'].loc[i] = 1

        return df

    def buy_past_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df.tail(200).iterrows():
            df['percentage'].loc[i] = self.search.percentage(df[i - self.n:i - 24]) + 2

            if df.loc[i]['ex_min_percentage'] and \
                    df.loc[i]['ex_min_percentage'] < -df.loc[i]['percentage']:

                candles = 0

                for x in range(i - 48, i):
                    if x > 1 and df.loc[x]['rsi_7'] < 25:
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
                        candles = i - x

                        df['buy_stride'].loc[i] = candles
                        df['buy_past_rsi'].loc[i] = df.loc[x]['buy_past_rsi']

                        df['market'].loc[i] = self.search.market(df=df, n=i)
        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['buy_stride'] > 3) & (df['buy_stride'] < 8) &
            (df['buy_past_rsi'] > 0)
            ,
            'buy'
        ] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] > 88) |
            (df['rsi_30'] > 73),
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
