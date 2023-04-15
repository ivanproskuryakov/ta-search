from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearchLevelH15m import TaSearchLevelH15m

dataset_builder = DatasetBuilder()
strategy = TaSearchLevelH15m({})

def test_ALGO_USDT_5m():
    path = 'fixture/ALGO_USDT_5m_1669852800.0_1670112000.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})
    df = strategy.populate_entry_trend(df, {})
    df = strategy.populate_exit_trend(df, {})

    assert df.loc[690]['o'] == 0.24155000000000001
    assert df.loc[690]['c'] == 0.24125000000000002
    assert df.loc[690]['open'] == 0.24150000000000002
    assert df.loc[690]['close'] == 0.241
    assert df.loc[690]['buy_short'] == 0
    assert df.loc[690]['buy_short2'] == 0
    assert df.loc[690]['buy_long'] == 0
    assert df.loc[690]['buy_long2'] == 1