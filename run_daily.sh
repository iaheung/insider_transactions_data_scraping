#!/bin/bash

echo "Saving insider transaction data from yesterday"

cd scripts || { echo "Failed to navigate to the scripts directory"; exit 1; }

source ~/anaconda3/etc/profile.d/conda.sh
conda activate your_env_name

python daily_save_insider.py
python ticker_prices.py

echo "Data saved successfully"
