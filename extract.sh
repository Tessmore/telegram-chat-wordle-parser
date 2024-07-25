#!/bin/bash

set -e

# find ./export/ -name "*.html" finds the HTML files.
# sort -V sorts the files in alphanumeric order.
# xargs -I {} sh -c 'python main.py "{}"' passes each sorted file to your Python script.

find ./export/ -name "*.html" | sort -V | xargs -I {} sh -c 'python main.py "{}"'
