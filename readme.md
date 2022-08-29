## Description

Trade entry indicator detection library 

### Installation

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

### Commands

```
python download.py AUTO 1h 1660485600 1660572000
python download.py AUTO 5m 1660485600 1660572000
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

```