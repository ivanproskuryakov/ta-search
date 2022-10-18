from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearch30m import TaSearch30m

dataset_builder = DatasetBuilder()
strategy = TaSearch30m({})


def test_bnb():
    path = 'fixture/30m/BNB_USDT_30m_1665169200.0_1666112400.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})

    print(df)
