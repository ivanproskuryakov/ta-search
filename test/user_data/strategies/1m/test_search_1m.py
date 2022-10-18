from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearch1m import TaSearch1m

dataset_builder = DatasetBuilder()
strategy = TaSearch1m({})


def test_bnb():
    path = 'fixture/1m/BNB_USDT_1m_1666072800.0_1666134000.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})

    print(df)

#
# def test_eth():
#     path = 'fixture/1m/ETH_USDT_1m_1662271200.0_1662285600.0.json'
#
#     df = dataset_builder.from_file(path)
#     df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
#     df = strategy.populate_indicators(df, {})
#
#     min = df.query('ex_min_percentage != ""')
#     max = df.query('ex_max_percentage != ""')
#
#     assert len(min) == 2
#     assert len(max) == 3
#
