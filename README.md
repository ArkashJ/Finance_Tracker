Project to load pdfs from my local machine, read financial data, collate them into 4 tables and do financial
analysis on them

### Run Following to Save Packages
```
pip3 freeze > requirements.txt
```

### Load Packages by Running:
```
 ~ pip install -r requirements.txt
```

## TODO
- Make an account on financialmodelingprep.com
- Get API key
- Make a ```config.py``` file in the root directory
- Store your key, the url ```https://financialmodelingprep.com/api``` and version ```v3``` in the config file
(The financial statement apis use version v3 but some others use v4)

## Run the following to create a virtual environment
```
python3 -m venv venv
```

## Run the following to activate the virtual environment
```
source venv/bin/activate
```

## Run the following to deactivate the virtual environment
```
deactivate
```

