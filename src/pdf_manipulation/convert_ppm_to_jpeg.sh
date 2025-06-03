#!/bin/bash

# Check if folder is provided and exists
if [ -z "$1" ] || [ ! -d "$1" ]; then
  echo "Usage: $0 <folder_with_ppm_files>"
  exit 1
fi

folder="$1"

shopt -s nullglob

for file in "$folder"/*.ppm; do
  filename=$(basename "$file")
  output="${filename%.ppm}.jpg"
  magick "$file" "$folder/$output" && rm "$file"
  echo "Converted and removed $file"
done
