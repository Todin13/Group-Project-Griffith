#!/bin/bash

usage() {
  echo "Usage: $0 -i input.txt [-o output.txt]"
  exit 1
}

# Default output
OUTPUT="cleaned_output.txt"

# Parse options
while getopts ":i:o:" opt; do
  case $opt in
    i) INPUT="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    *) usage ;;
  esac
done

# If input not set by -i, check positional param
if [ -z "$INPUT" ]; then
  if [ -n "$1" ]; then
    INPUT="$1"
  else
    usage
  fi
fi

# Check if input file exists
if [ ! -f "$INPUT" ]; then
  echo "Input file '$INPUT' not found."
  exit 1
fi

cat "$INPUT" \
  | sed 's/-$//' \
  | awk 'BEGIN{ORS="";} NF{print $0 " "}{print "\n"}' \
  | sed 's/  */ /g' \
  | sed '/^[[:space:]]*[0-9][0-9]*[[:space:]]*$/d' \
  | sed '/^[[:space:]]*[A-Z0-9[:punct:][:space:]]\{2,\}$/d' \
  | sed ':a; /^[[:space:]]*$/ { $d; N; ba }' \
  > "$OUTPUT"

echo "Cleaned text saved to $OUTPUT"

