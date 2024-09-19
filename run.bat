@ECHO OFF

ECHO Saving all insider transaction data

cd scripts

CALL conda activate csc371
python save_insider.py

ECHO Data saved successfully
PAUSE
