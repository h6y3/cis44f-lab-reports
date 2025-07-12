#!/bin/bash

echo "Lab Report Generator - Installation Script"
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "lab_report_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv lab_report_env
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source lab_report_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete!"
echo ""
echo "To use the lab report generator:"
echo "1. Run: source lab_report_env/bin/activate"
echo "2. Run: python3 generate_lab_report.py <lab_directory>"