from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearch5m import TaSearch5m

dataset_builder = DatasetBuilder()
strategy = TaSearch5m({})


def test_bnb():
    path = 'fixture/1m/BNB_USDT_1m_1666054800.0_1666112400.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})

    print(df)