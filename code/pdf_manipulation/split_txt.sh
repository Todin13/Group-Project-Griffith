#!/bin/bash

# Check arguments (4 mandatory, 1 optional)
if [[ $# -lt 4 || $# -gt 5 ]]; then
    echo "Usage: $0 <input_file.txt> <output_prefix> <split_pattern> <start_line> [end_line]"
    echo "Example: $0 book.txt chapter '^Chapter ' 10 5000"
    exit 1
fi

INPUT="$1"
PREFIX="$2"
PATTERN="$3"
START_LINE="$4"
OUTPUT_DIR="${PREFIX}s"

# Optional end line
if [[ $# -eq 5 ]]; then
    END_LINE="$5"
else
    END_LINE=0
fi

mkdir -p "$OUTPUT_DIR"

# Track lines
LINE_NUM=0
COUNT=0
declare -A LINE_CONTENT
INTRO_LINES=()
CONCLUSION_LINE=0
BIBLIO_LINE=0

# Step 1: Read all lines, collect intro and store line content, stop reading at END_LINE if specified
while IFS= read -r line; do
    ((LINE_NUM++))
    LINE_CONTENT[$LINE_NUM]="$line"

    # Stop if we've read up to optional END_LINE
    if [[ $END_LINE -gt 0 && $LINE_NUM -ge $END_LINE ]]; then
        break
    fi

    if (( LINE_NUM < START_LINE )); then
        if [[ "$line" =~ [Ii]ntroduction || "$line" =~ [Pp]reface ]]; then
            INTRO_LINES+=("$LINE_NUM")
        fi
    elif (( LINE_NUM >= START_LINE )); then
        if [[ $CONCLUSION_LINE -eq 0 && "$line" =~ [Cc]onclusion ]]; then
            CONCLUSION_LINE=$LINE_NUM
        elif [[ $BIBLIO_LINE -eq 0 && "$line" =~ [Bb]ibliograph(y|ie) ]]; then
            BIBLIO_LINE=$LINE_NUM
        fi
    fi
done < "$INPUT"

# If no END_LINE specified, use last line read
if [[ $END_LINE -eq 0 ]]; then
    END_LINE=$LINE_NUM
fi

# Step 2: Introduction & Summary logic
if (( ${#INTRO_LINES[@]} >= 1 )); then
    FIRST_INTRO=${INTRO_LINES[0]}
    LAST_INTRO=${INTRO_LINES[-1]}

    INTRO_BUFFER=""
    for ((i=LAST_INTRO; i<START_LINE; i++)); do
        INTRO_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
    done
    echo -n "$INTRO_BUFFER" > "${OUTPUT_DIR}/introduction.txt"

    if (( ${#INTRO_LINES[@]} >= 2 )); then
        SUMMARY_BUFFER=""
        for ((i=FIRST_INTRO; i<=LAST_INTRO; i++)); do
            SUMMARY_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
        done
        echo -n "$SUMMARY_BUFFER" > "${OUTPUT_DIR}/summary.txt"
    fi
fi

# Step 3: Split chapters (until Conclusion or end)

if (( CONCLUSION_LINE > 0 )); then
    END_SPLIT_LINE=$(( CONCLUSION_LINE - 1 ))
elif (( BIBLIO_LINE > 0 )); then
    END_SPLIT_LINE=$(( BIBLIO_LINE - 1 ))
else
    END_SPLIT_LINE=$END_LINE
fi

BUFFER=""
COUNT=0

for ((i=START_LINE; i<=END_SPLIT_LINE; i++)); do
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

if [[ -n "$BUFFER" ]]; then
    echo "$BUFFER" > "${OUTPUT_DIR}/${PREFIX}${COUNT}.txt"
fi

# Step 4: Save Conclusion (between Conclusion and Bibliography)
if (( CONCLUSION_LINE > 0 && (BIBLIO_LINE == 0 || BIBLIO_LINE > CONCLUSION_LINE) )); then
    CONCLUSION_BUFFER=""
    LAST_CONCL_LINE=$(( BIBLIO_LINE > 0 ? BIBLIO_LINE - 1 : END_LINE ))

    for ((i=CONCLUSION_LINE; i<=LAST_CONCL_LINE; i++)); do
        CONCLUSION_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
    done
    echo -n "$CONCLUSION_BUFFER" > "${OUTPUT_DIR}/conclusion.txt"
fi

# Step 5: Save Bibliography (from Bibliography to end)
if (( BIBLIO_LINE > 0 )); then
    BIBLIO_BUFFER=""
    for ((i=BIBLIO_LINE; i<=END_LINE; i++)); do
        BIBLIO_BUFFER+="${LINE_CONTENT[$i]}"$'\n'
    done
    echo -n "$BIBLIO_BUFFER" > "${OUTPUT_DIR}/bibliography.txt"
fi

# ✅ Final report
echo "✅ Done."
echo "→ Chapters created: $COUNT"
[[ -f "${OUTPUT_DIR}/introduction.txt" ]] && echo "→ Saved: introduction.txt"
[[ -f "${OUTPUT_DIR}/summary.txt" ]] && echo "→ Saved: summary.txt"
[[ -f "${OUTPUT_DIR}/conclusion.txt" ]] && echo "→ Saved: conclusion.txt"
[[ -f "${OUTPUT_DIR}/bibliography.txt" ]] && echo "→ Saved: bibliography.txt"

