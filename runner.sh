#!/bin/bash

input_dir="images"
output_dir="final"

for file in "$input_dir"/*.tif; do
    filename=$(basename "$file")
    filename_without_ext="${filename%.*}"
    output_file="$output_dir/$filename_without_ext.jpg"
    python3 main.py "$file" "$output_file" --depth 5 --width 10
done

for file in "$input_dir"/*.jpg; do
    filename=$(basename "$file")
    filename_without_ext="${filename%.*}"
    output_file="$output_dir/$filename_without_ext.jpg"
    python3 main.py "$file" "$output_file" --depth 3 --width 10
done