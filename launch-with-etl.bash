#!/bin/sh
set -e

# launch file for fisheyesea
# bash launch.bash

echo 🚀 Launching fisheyesea !

export WITH_ETL=true

cd src && uv run uvicorn main:app --reload --log-config ../config/logging.yml