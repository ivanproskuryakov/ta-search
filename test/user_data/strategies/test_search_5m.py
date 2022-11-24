from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearch5m import TaSearch5m

dataset_builder = DatasetBuilder()
strategy = TaSearch5m({})


def test_ldo():
    path = 'fixture/LDO_USDT_5m_1666310400.0_1667210709.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})
    df = strategy.populate_buy_trend(df, {})
    df = strategy.populate_sell_trend(df, {})

    assert df.loc[2545]['buy'] == 1
