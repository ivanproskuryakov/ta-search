## Description
![CI](https://github.com/ivanproskuryakov/ta-search/workflows/CI/badge.svg)


Entry indicator detection library and strategies for FreqTrade trade bot, see `user_data/strategies` directory.  

```
freqtrade trade --config config.usdt.5m.json --strategy TaSearch5m --db-url sqlite:///search5mStrategy.sqlite
freqtrade trade --config config.usdt.30m.json --strategy TaSearch30m --db-url sqlite:///search30mStrategy.sqlite
```

![model predict](doc/freqtrade_1m.png)

### Installation

For development copy the repository using git clone and install package requirements with commands below.

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

### Testing

The command to download time series data for an interval
```
python download.py LDO 5m 1666310400 1667210709
python download.py LDO 30m 1666310400 1667210709

python download.py TWT 5m 1671926400 1672099200
```

Run tests
```
python -m pytest test
python -m pytest -s test/user_data/strategies/test_search_5m.py
python -m pytest -s test/user_data/strategies/test_search_30m.py
```