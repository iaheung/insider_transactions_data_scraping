@ECHO OFF

ECHO Saving all insider transaction data

cd scripts
IF ERRORLEVEL 1 (
    ECHO Failed to navigate to the scripts directory
    EXIT /B 1
)

CALL conda activate your_env_name

python save_insider.py
python data_processing.py

ECHO Data saved successfully
PAUSE
