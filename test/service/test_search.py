import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search import Search

dataset_builder = DatasetBuilder()
search = Search()

pd.set_option('display.max_rows', 100000)


def test_find_peaks_auto_1h():
    path = 'fixture/AUTO_USDT_1h_1660485600.0_1660572000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["price_close"]]
    df = search.find_peaks(df)

    print(df)


def test_find_peaks_ldo_1h():
    path = 'fixture/LDO_USDT_1h_1660521600.0_1661212800.0.json'

    df = dataset_builder.from_file(path)
    df = df[["price_close"]]
    df = search.find_peaks(df)

    print(df)
