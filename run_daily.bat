@ECHO OFF

ECHO Saving insider transaction data from yesterday

cd scripts

CALL conda activate your_env_name

python live_save_insider.py
python ticker_prices.py

ECHO Data saved successfully
PAUSE
