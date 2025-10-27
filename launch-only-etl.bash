#!/bin/sh
set -e

# launch file for fisheyesea
# bash launch.bash

echo "🚀 Launching fisheyesea (ONLY ETL VERSION) !"

cd src && uv run only_etl.py