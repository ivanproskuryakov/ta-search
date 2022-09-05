import pandas as pd

from datetime import datetime


class DatasetBuilder:
    def from_file(self, path: str) -> pd.DataFrame:
        df = pd.read_json(path)

        df['date'] = df['time_open'].apply(lambda x: datetime.utcfromtimestamp(x))

        return df
