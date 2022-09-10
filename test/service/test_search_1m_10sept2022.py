import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search1m import Search1m

dataset_builder = DatasetBuilder()
search = Search1m(n=60, p=1)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_ldo():
    path = 'fixture/LDO_USDT_1m_1662674400.0_1662847200.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    # df = df[0:1605]
    df = search.find_peaks(df)

    print(df)

def test_rose():
    path = 'fixture/ROSE_USDT_1m_1662674400.0_1662847200.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = df[0:1650]
    df = search.find_peaks(df)

    print(df)