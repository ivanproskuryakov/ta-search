import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search1m import Search1m

dataset_builder = DatasetBuilder()
search = Search1m(n=60, p=1)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_find_peaks_one_1m():
    path = 'fixture/1m/ONE_USDT_1m_1662361200.0_1662411600.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)
