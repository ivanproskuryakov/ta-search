## Description

Trade entry indicator detection library 

### Installation

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

# todo 
Check the last two lows 



### Commands

```
python download.py AUTO 1h 1660485600 1660572000

python download.py LDO 1m 1663027200 1663113600
```

```

freqtrade trade --config config.usdt.json --strategy TaSearch5mN48P2 --db-url sqlite:///TaSearch5mN48P2.sqlite
freqtrade trade --config config.usdt.json --strategy TaSearch5mN96P5 --db-url sqlite:///TaSearch5mN96P5.sqlite
freqtrade trade --config config.usdt.1m.json --strategy TaSearch1mN60P05 --db-url sqlite:///TaSearch1mN60P05.sqlite
```

### Testing

Same as with training, tests require `ta_test` db for prevention of spoiling training or dev databases.

```
psql -U postgres
create database ta_test;
``` 

Running tests

```
python -m pytest test
python -m pytest --log-cli-level DEBUG -s test/service/test_dataset_builder.py
python -m pytest -s test/service/test_search_1h.py
python -m pytest -s test/service/test_search_5m.py
python -m pytest -s test/service/test_search_1m.py

```