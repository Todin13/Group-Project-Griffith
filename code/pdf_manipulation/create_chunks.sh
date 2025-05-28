#!/bin/bash

DIR="${1:-.}"
OUTPUT="pinecone_records.json"

# Function to split text into chunks of max 250 words ending at a period
split_text() {
    local text="$1"
    local max_words=50

    echo "$text" | perl -e '
        use strict;
        use warnings;

        my $text = do { local $/; <STDIN> };
        $text =~ s/\n/ /g;
        $text =~ s/\s+/ /g;

        my @sentences = split(/(?<=\.)\s+/, $text);

        my @chunks;
        my $current_chunk = "";
        my $current_words = 0;

        foreach my $sent (@sentences) {
            my $sent_words = scalar(split(/\s+/, $sent));

            if ($current_words + $sent_words <= '"$max_words"') {
                $current_chunk .= $sent . " ";
                $current_words += $sent_words;
            } else {
                $current_chunk =~ s/\s+$//;
                push @chunks, $current_chunk;
                $current_chunk = $sent . " ";
                $current_words = $sent_words;
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

    # Get chunks separated by |||
    chunks=$(split_text "$content")

    # Split chunks into array using ||| as delimiter
    IFS='|||' read -r -a chunk_array <<< "$chunks"

    idx=1
    for chunk in "${chunk_array[@]}"; do
    
         # Remove leading/trailing whitespace and newlines from chunk
    clean_chunk=$(echo "$chunk" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    # Skip if empty after cleaning
    if [[ -z "$clean_chunk" ]]; then
        continue
    fi

    # # Escape chunk content for JSON using cleaned chunk
    # escaped_chunk=$(echo "$clean_chunk" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')


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
