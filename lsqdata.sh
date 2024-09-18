#!/bin/bash

# Define the project directory
PROJECT_DIR="$HOME/logseq-data-converter"

# Check if all required arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_file> <output_format> [verbose]"
    exit 1
fi

# Get the absolute path of the input file
INPUT_FILE=$(realpath "$1")

# Shift the arguments to remove the input file
shift

# Change to the project directory
cd "$PROJECT_DIR"

# Source the virtual environment
source "$PROJECT_DIR/bin/activate"

# Run the Python script with arguments
python -m main "$INPUT_FILE" "$@"

# Deactivate the virtual environment
deactivate
