import math

from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearchLevelJ15m import TaSearchLevelJ15m

dataset_builder = DatasetBuilder()
strategy = TaSearchLevelJ15m({})

def test_ALGO_USDT_5m():
    path = 'fixture/ALGO_USDT_5m_1669852800.0_1670112000.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})
    df = strategy.populate_entry_trend(df, {})
    df = strategy.populate_exit_trend(df, {})

    assert df.loc[302]['o'] == 0.23645
    assert df.loc[302]['c'] == 0.236075
    assert df.loc[302]['open'] == 0.23600000000000002
    assert df.loc[302]['close'] == 0.2361
    assert df.loc[302]['min_local'] == 0.236075
    assert math.isnan(df.loc[302]['max_local'])
