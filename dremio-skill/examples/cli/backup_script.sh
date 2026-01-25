#!/bin/bash
# Dremio Catalog Backup & Export Script
# Usage: ./backup_script.sh <space_name> <output_dir>

SPACE_NAME=$1
OUTPUT_DIR=$2
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Check for CLI tool
if ! command -v dremio &> /dev/null; then
    echo "Error: dremio-cli is not installed."
    echo "Run: pip install dremio-cli"
    exit 1
fi

# Check arguments
if [ -z "$SPACE_NAME" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: ./backup_script.sh <space_name> <output_dir>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Starting backup for Space: $SPACE_NAME"

# 1. Export Content (Tags, Wikis, View Definitions)
# Note: This uses the CLI's catalog listing feature and saves to JSON
echo "Exporting catalog metadata..."
dremio --output json catalog get-by-path "$SPACE_NAME" > "$OUTPUT_DIR/${SPACE_NAME}_meta_${TIMESTAMP}.json"

# 2. List all datasets in the space (Inventory)
echo "Generating dataset inventory..."
# Using jq to filter if available, otherwise just raw dump
dremio --output json catalog list | grep "$SPACE_NAME" > "$OUTPUT_DIR/${SPACE_NAME}_inventory_${TIMESTAMP}.json"

echo "Backup complete. Files saved to $OUTPUT_DIR"
ls -l "$OUTPUT_DIR"
