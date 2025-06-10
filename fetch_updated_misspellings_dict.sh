#!/bin/bash

# Define the output file
OUTPUT_FILE="src/constants/misspellings"

# Curl the HTML content, then process it to extract only the first word before "->"
curl "https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines" \
  | sed -n '/<pre>/,/<\/pre>/p' \
  | grep -v '^<' \
  | grep -v '^$' \
  | sed 's/->.*//' \
  | grep -v "^ok$" \
  >> "${OUTPUT_FILE}"