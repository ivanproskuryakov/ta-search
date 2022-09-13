from src.service.dataset_builder import DatasetBuilder
from src.service.search import Search

dataset_builder = DatasetBuilder()
search = Search()


def test_from_file():
    path = 'fixture/AUTO_USDT_1h_1660485600.0_1660572000.0.json'
    df = dataset_builder.from_file(path)

    assert df.iloc[0]['trades'] == 320.0
