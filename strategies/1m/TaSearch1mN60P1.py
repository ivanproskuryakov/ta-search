from SearchStrategy import SearchStrategy


class TaSearch1mN60P1(SearchStrategy):
    n = 60
    p = 1.2
    minimal_roi = {
        "0": 0.01
    }
    stoploss = -0.25
