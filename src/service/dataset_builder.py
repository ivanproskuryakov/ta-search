import pandas as pd


class DatasetBuilder:
    def from_file(self, path: str):
        df = pd.read_json(path)

        return df
