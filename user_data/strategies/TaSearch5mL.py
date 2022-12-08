import pandas as pd

from freqtrade.strategy.interface import IStrategy
from datetime import datetime
from freqtrade.persistence import Trade
from typing import Optional

from taSearch import TaSearch


class TaSearch5mL(IStrategy):
    search: TaSearch
    n: int
    p: float

    n = 144
    p = 5
    minimal_roi = {
        "0": 0.02 * 5
    }
    stoploss = -0.05 * 5
    timeframe = '5m'

    # 100 = 1000 * 10%

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
                for x in range(i - 64, i):
                    if x > 1 and df.loc[x]['rsi_7'] < 25:
                        c += 1

                        df['buy_past_rsi'].loc[x] = c
                        df['buy_past_rsi'].loc[i] = c

        return df

    def buy_stride(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df[::-1].iterrows():
            if 15 < df.loc[i]['rsi_7'] < 40:
                for x in range(i - 24, i):
                    if x > 1 \
                            and df.loc[x]['ex_min_percentage'] \
                            and df.loc[x]['ex_min_percentage'] < -self.p:
                        df['buy_stride'].loc[i] = i - x
                        df['buy_past_rsi'].loc[i] = df.loc[x]['buy_past_rsi']

                        df['market'].loc[i] = self.search.market(df=df, n=i)
        return df

    def populate_entry_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['buy_stride'] > 5) & (df['buy_stride'] < 10) &
            (df['buy_past_rsi'] > 5) &
            (df['market'] == -1),
            'buy'
        ] = 1

        return df

    def populate_exit_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] > 85) |
            ((df['rsi_7'] > 70) & (df['rsi_30'] > 62)),
            'sell'
        ] = 1

        return df

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return 5

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:

        profit = trade.calc_profit_ratio(rate)

        if exit_reason == 'exit_signal' and profit < 0:
            return False

        return True
