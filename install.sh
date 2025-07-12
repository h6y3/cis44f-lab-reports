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

# Generate configuration file
if [ ! -f "config.json" ]; then
    echo "Setting up configuration..."
    echo ""
    read -p "Enter your full name: " student_name
    read -p "Enter course code (default: CIS44F): " course_code
    read -p "Enter school name (default: De Anza College): " school_name
    
    # Use defaults if empty
    course_code=${course_code:-CIS44F}
    school_name="${school_name:-De Anza College}"
    
    # Create config.json
    cat > config.json << EOF
{
  "student_name": "$student_name",
  "course_code": "$course_code",
  "school": "$school_name"
}
EOF
    
    echo ""
    echo "Configuration saved to config.json"
    echo "You can edit this file anytime to change your information."
else
    echo "Configuration file already exists (config.json)"
fi

echo ""
echo "To use the lab report generator:"
echo "1. Run: source lab_report_env/bin/activate"
echo "2. Run: python3 generate_lab_report.py <lab_directory>"
echo ""
echo "Your reports will use the name and course information from config.json"