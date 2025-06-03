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
IMAGE_DESC_FILE="results/image_description.txt"
> "$IMAGE_DESC_FILE"  # clear or create

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
./src/pdf_manipulation/split_txt.sh Griffith\ College\ 200\ Years.txt result "Chapter " 119 2720

# cleaning files one by one
for file in results/*; do
  [[ -f "$file" ]] || continue
  echo "Processing $file"

  # run cleaning scrit
  ./src/pdf_manipulation/clean.sh "$file"
done

# delete files without "_cleaned" if enabled
if [ "$DELETE_UNCLEANED" = true ]; then
  echo "Deleting files without '_cleaned' in filename..."
  find results/ -type f ! -name '*_cleaned*' -exec rm {} +
else
  echo "Keeping files without '_cleaned' in filename."
fi

# Initialize counter
count=1

# Rename and trim files starting with 'result_'
for file in results/result*; do
  # Check if it's a file
  if [[ ! -f "$file" ]]; then
    continue
  fi

  # Extract second line, normalize spacing, and replace spaces with underscores
  newname=$(sed -n '2p' "$file" | tr -d '\r\n' | tr -s ' ' | tr ' ' '_')

  if [ -z "$newname" ]; then
    echo "Skipping $file, second line empty"
    continue
  fi

  # Trim the file starting from the third line
  tail -n +3 "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"

  # Construct new filename with count prefix
  numbered_name="results/${count}_${newname}.txt"

  # Rename the file
  mv "$file" "$numbered_name"
  echo "Renamed and trimmed $file -> $numbered_name"

  # Increment counter
  ((count++))
done

for file in results/*; do
  [[ -f "$file" ]] || continue
  [[ "$(basename "$file")" == "summary_cleaned.txt" ]] && continue
  echo "Processing $file"

  # perl -00 -ne 'print "PARAGRAPH:\n[$_]\n\n"' "$file" >> paraph # debug only

  # extract image descriptions and append to central file
  perl -00 -ne '
    my $p = $_;
    my $lines = () = $p =~ /\n/g;
    my $words = scalar split /\s+/, $p;

    if (
      ($lines < 3 && $words < 16) ||  # one-line short paragraph — always match
      (
        $words < 50 &&
        $lines < 12 &&
        (
          $p =~ /\(([^)]*(Ireland|Courtesy|Irish)[^)]*)\)/i ||
          $p =~ /\b(view of|aerial view|above:|right:|left:|below:|pictured|caption reads:)/i
        )
      )
    ) {
      print $p;
    }
  ' "$file" >> "$IMAGE_DESC_FILE"

  # remove them from original and overwrite
  perl -00 -ne '
    my $p = $_;
    my $lines = () = $p =~ /\n/g;
    my $words = scalar split /\s+/, $p;

    unless (
      ($lines < 3 && $words < 16) ||  # one-line short paragraph — always remove
      (
        $words < 50 &&
        $lines < 12 &&
        (
          $p =~ /\(([^)]*(Ireland|Courtesy|Irish)[^)]*)\)/i ||
          $p =~ /\b(view of|aerial view|above:|right:|left:|below:|pictured|caption reads:)/i
        )
      )
    ) {
      print $p;
    }
  ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"

done

./src/pdf_manipulation/create_chunks.sh results/
