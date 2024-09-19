@ECHO OFF

ECHO Saving all insider transaction data

cd scripts

CALL conda activate your_env_name
python save_insider.py

ECHO Data saved successfully
PAUSE
