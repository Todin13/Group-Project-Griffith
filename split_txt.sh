#!/bin/bash

# Check arguments
if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <input_file.txt> <output_prefix> <split_pattern> <start_line>"
    echo "Example: $0 book.txt chapter '^Chapter ' 10"
    exit 1
fi

# Arguments
INPUT="$1"
PREFIX="$2"
PATTERN="$3"
START_LINE="$4"
OUTPUT_DIR="${PREFIX}s"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Line tracking
LINE_NUM=0
COUNT=0
BUFFER=""
LINES_BEFORE_START=()

# Track intro/preface occurrences
INTRO_LINES=()
declare -A LINE_CONTENT

# Pass 1: Read all lines and cache
while IFS= read -r line; do
    ((LINE_NUM++))
    LINE_CONTENT[$LINE_NUM]="$line"

    if (( LINE_NUM < START_LINE )); then
        LINES_BEFORE_START+=("$LINE_NUM")

        if [[ "$line" =~ [Ii]ntroduction || "$line" =~ [Pp]reface ]]; then
            INTRO_LINES+=("$LINE_NUM")
        fi
    fi
done < "$INPUT"

# Handle introduction / summary
if (( ${#INTRO_LINES[@]} >= 1 )); then
    FIRST_INTRO=${INTRO_LINES[0]}
    LAST_INTRO=${INTRO_LINES[-1]}

    # Build introduction buffer from LAST_INTRO to START_LINE - 1
    INTRO_BUFFER=""
    for ((i=LAST_INTRO; i<START_LINE; i++)); do
        INTRO_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
    done
    echo -n "$INTRO_BUFFER" > "${OUTPUT_DIR}/introduction.txt"
    echo "📝 Saved last introduction section to '${OUTPUT_DIR}/introduction.txt'"

    # If two or more intros, build summary from FIRST_INTRO to LAST_INTRO
    if (( ${#INTRO_LINES[@]} >= 2 )); then
        SUMMARY_BUFFER=""
        for ((i=FIRST_INTRO; i<LAST_INTRO; i++)); do
            SUMMARY_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
        done
        echo -n "$SUMMARY_BUFFER" > "${OUTPUT_DIR}/summary.txt"
        echo "📝 Saved summary section to '${OUTPUT_DIR}/summary.txt'"
    fi
fi

# Pass 2: Chapter splitting from START_LINE onward
COUNT=0
BUFFER=""
for ((i=START_LINE; i<=LINE_NUM; i++)); do
    line="${LINE_CONTENT[$i]}"
    if [[ "$line" =~ $PATTERN ]]; then
        if [[ $COUNT -ne 0 ]]; then
            echo "$BUFFER" > "${OUTPUT_DIR}/${PREFIX}${COUNT}.txt"
        fi
        ((COUNT++))
        BUFFER="$line"
    else
        BUFFER+=$'\n'"$line"
    fi
done

# Write final chapter
if [[ -n "$BUFFER" ]]; then
    echo "$BUFFER" > "${OUTPUT_DIR}/${PREFIX}${COUNT}.txt"
fi

echo "✅ Done. Created $COUNT chapter files in '$OUTPUT_DIR/', starting from line $START_LINE."

