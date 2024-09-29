#!/bin/bash

echo "Saving all insider transaction data"

cd scripts || { echo "Failed to navigate to scripts directory"; exit 1; }

source ~/anaconda3/etc/profile.d/conda.sh
conda activate your_env_name

python save_insider.py

echo "Data saved successfully"
