#!/bin/bash

DIR="${1:-.}"
OUTPUT="pinecone_records.json"

# Function to split text into chunks of max 50 words ending at a period
split_text() {
    local text="$1"
    local min_words=50

    echo "$text" | perl -e '
        use strict;
        use warnings;

        # Read all of STDIN
        my $text = do { local $/; <STDIN> };

        # Replace newlines with custom marker
        $text =~ s/\n/ <<<NL>>> /g;

        # Normalize whitespace
        $text =~ s/\s+/ /g;

        # Split at the end of paragraph
        # Split only at: period followed by optional spaces and <<<NL>>>
        my @sentences = split(/(?<=\.)\s*<<<NL>>>/, $text);

        my @chunks;
        my $current_chunk = "";
        my $current_words = 0;

        foreach my $sent (@sentences) {
            $sent =~ s/<<<NL>>>//g;      # Clean marker
            $sent =~ s/^\s+|\s+$//g;     # Trim whitespace
            next unless $sent;

            my $sent_words = scalar(split(/\s+/, $sent));

            $current_chunk .= $sent . " ";
            $current_words += $sent_words;

            if ($current_words > '"$min_words"') {
                $current_chunk =~ s/\s+$//;
                push @chunks, $current_chunk;

                $current_chunk = "";
                $current_words = 0;
            }

        }

        $current_chunk =~ s/\s+$//;
        push @chunks, $current_chunk if $current_chunk ne "";

        print join("|||", @chunks);
    '
}

echo "[" > "$OUTPUT"
first=true

# Process all .txt files in the directory
find "$DIR" -type f -name "*.txt" | while read -r filepath; do
    filename=$(basename "$filepath" .txt)
    content=$(<"$filepath")

    # Skip completely if image_description or summary_cleaned
    if [[ "$filename" == "image_description" || "$filename" == "summary_cleaned" ]]; then
        continue
    fi

    # Special case: handle bibliography_cleaned as a single cleaned entry
    if [[ "$filename" == "bibliography_cleaned" ]]; then
        clean_chunk=$(echo "$content" | tr -d '\r' | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        if [[ -n "$clean_chunk" ]]; then
            if $first; then
                first=false
            else
                echo "," >> "$OUTPUT"
            fi

            echo "  {" >> "$OUTPUT"
            echo "    \"_id\": \"${filename}_1\"," >> "$OUTPUT"
            echo "    \"chunk_text\": \"$clean_chunk\"," >> "$OUTPUT"
            echo "    \"category\": \"$filename\"" >> "$OUTPUT"
            echo "  }" >> "$OUTPUT"
        fi
        continue
    fi

    # Process normally: split into chunks
    chunks=$(split_text "$content")
    IFS='|||' read -r -a chunk_array <<< "$chunks"

    idx=1
    for chunk in "${chunk_array[@]}"; do
        clean_chunk=$(echo "$chunk" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

        # Skip empty chunks
        if [[ -z "$clean_chunk" ]]; then
            continue
        fi

        if $first; then
            first=false
        else
            echo "," >> "$OUTPUT"
        fi

        echo "  {" >> "$OUTPUT"
        echo "    \"_id\": \"${filename}_${idx}\"," >> "$OUTPUT"
        echo "    \"chunk_text\": \"$clean_chunk\"," >> "$OUTPUT"
        echo "    \"category\": \"$filename\"" >> "$OUTPUT"
        echo "  }" >> "$OUTPUT"

        ((idx++))
    done
done

echo "]" >> "$OUTPUT"
echo "Records saved to $OUTPUT"
