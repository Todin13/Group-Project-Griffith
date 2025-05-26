#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input-file>"
    exit 1
fi

input="$1"
filename_no_ext="${input%.*}"
output="${filename_no_ext}_cleaned.txt"
temp_step1=$(mktemp)
temp_step2=$(mktemp)

# Step 1: Merge single-letter lines followed by blank and another line
awk '
{
    buffer[NR] = $0
}
END {
    for (i = 1; i <= NR; i++) {
        if (buffer[i] ~ /^[[:space:]]*[a-zA-Z][[:space:]]*$/ &&
            buffer[i+1] ~ /^[[:space:]]*$/ &&
            i+2 <= NR)
        {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", buffer[i])
            print buffer[i] buffer[i+2]
            i += 2
        } else {
            print buffer[i]
        }
    }
}
' "$input" > "$temp_step1"

# Step 2: Remove ^L, lines with only uppercase (plus numbers/punct), and lines with only numbers (preserve blank lines)
sed -E 's/\f//g' "$temp_step1" | awk '
{
    if ($0 ~ /^[[:space:]]*$/) {
        print $0
    } else if ($0 !~ /[a-z]/ && $0 ~ /^[A-Z0-9[:punct:][:space:]]*$/) {
        next
    } else if ($0 ~ /^[[:space:]]*[0-9]+[[:space:]]*$/) {
        next
    } else {
        print $0
    }
}
' > "$temp_step2"

# Step 3: Recursively merge single-word lines with the next line
awk '
function count_words(s) {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
    split(s, words, /[[:space:]]+/)
    return length(words)
}

{
    lines[NR] = $0
}
END {
    i = 1
    while (i <= NR) {
        current = lines[i]
        while (i < NR && count_words(current) == 1) {
            i++
            current = current " " lines[i]
        }
        print current
        i++
    }
}
' "$temp_step2" > "$output"

rm "$temp_step1" "$temp_step2"
echo "Cleaned file saved as $output"

