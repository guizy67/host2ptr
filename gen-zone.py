#!/usr/local/bin/python3

import json
import sys

# Check if the input file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: ./gen-zone.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# Load JSON data from the specified input file
with open(input_file) as f:
    data = json.load(f)

# Process the data and generate zone files
for item in data:
    zonefile = item[1]['zonename'] + '.db'
    record = str(item[1]['ptr_record']) + '\n'

    with open(zonefile, 'a') as zf:
        zf.write(record)

