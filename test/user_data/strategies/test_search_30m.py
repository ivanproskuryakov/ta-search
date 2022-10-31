from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearch30m import TaSearch30m

dataset_builder = DatasetBuilder()
strategy = TaSearch30m({})


def test_ldo():
    path = 'fixture/LDO_USDT_30m_1666310400.0_1667210709.0.json'

    df = dataset_builder.from_file(path)
    # df = df[0:477]
    # df = df[0:477]
    # df = df[0:485]

    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})
    df = strategy.populate_sell_trend(df, {})
    df = strategy.populate_buy_trend(df, {})

    df = df.drop(['open', 'high', 'low'], axis=1)

    print(df)