#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Initialize database if it doesn't exist
python setup_db.py
