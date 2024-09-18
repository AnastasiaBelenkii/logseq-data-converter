#!/bin/bash

# Define the project directory
PROJECT_DIR="$HOME/logseq-data-converter"

# Change to the project directory
cd "$PROJECT_DIR"

# Check if all required arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_file> <output_format> [verbose]"
    exit 1
fi

# Source the virtual environment
source "$PROJECT_DIR/bin/activate"

# Run the Python script with arguments
python -m main "$@"

# Deactivate the virtual environment
deactivate
