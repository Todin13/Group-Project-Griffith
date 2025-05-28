#!/bin/bash

show_help() {
  cat << EOF
Usage: $0 [OPTIONS]

Splits a text file by chapters, runs cleaning on each resulting file, and optionally deletes files
without '_cleaned' in their filename.

Options:
  --keep-uncleaned   Keep files without '_cleaned' in the filename (do NOT delete them).
  -h, --help         Show this help message and exit.

By default, files without '_cleaned' are deleted after cleaning.
EOF
}

# Default behavior
DELETE_UNCLEANED=true

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --keep-uncleaned)
      DELETE_UNCLEANED=false
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Use -h or --help for usage."
      exit 1
      ;;
  esac
done

# splitting by chapter, summary, conclusion, introduction
./code/pdf_manipulation/split_txt.sh Griffith\ College\ 200\ Years.txt result "Chapter " 119 2720

# cleaning files one by one
for file in results/*; do
  ./code/pdf_manipulation/clean.sh "$file"
done

# delete files without "_cleaned" if enabled
if [ "$DELETE_UNCLEANED" = true ]; then
  echo "Deleting files without '_cleaned' in filename..."
  find results/ -type f ! -name '*_cleaned*' -exec rm {} +
else
  echo "Keeping files without '_cleaned' in filename."
fi

# Rename and trim files starting with 'result_' in filename
for file in results/result*; do
  # check if it's a file (just in case)
  if [[ ! -f "$file" ]]; then
    continue
  fi

  newname=$(sed -n '2p' "$file" | tr -d '\r\n' | tr -s ' ' | tr ' ' '_')
  if [ -z "$newname" ]; then
    echo "Skipping $file, second line empty"
    continue
  fi

  tail -n +3 "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
  mv "$file" "results/${newname}.txt"
  echo "Renamed and trimmed $file -> results/${newname}.txt"
done

./code/pdf_manipulation/create_chunks.sh results/