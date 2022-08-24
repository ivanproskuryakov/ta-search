import numpy as np


class Utility:
    def round(self, n: float, decimals=10):
        return np.round(float(n), decimals)

    def diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return diff
