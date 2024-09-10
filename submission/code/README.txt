Image alignment and cropping can be done by running:

`python3 main.py "path_to_input_file" "path_to_output_file" --depth 5 --width 5`

The first parameter is required and represents the path to the input file to align.
The second parameter is required and represents the path of the output file to be saved.
The depth parameter is optional, defaulting to 5, and represents how many downsampled layers will be computed in the image pyramid.
The width parameter is optional, defaulting to 5, and represents how many pixels (in all directions) will be searched in each downsampled layer.

You can also run a bash script to generate all images:

```
#!/bin/bash

input_dir="images"
output_dir="v2/cropped"

for file in "$input_dir"/*.tif; do
    filename=$(basename "$file")
    filename_without_ext="${filename%.*}"
    output_file="$output_dir/$filename_without_ext.jpg"
    python3 main.py "$file" "$output_file" --depth 5 --width 5
done

for file in "$input_dir"/*.jpg; do
    filename=$(basename "$file")
    filename_without_ext="${filename%.*}"
    output_file="$output_dir/$filename_without_ext.jpg"
    python3 main.py "$file" "$output_file" --depth 3 --width 5
done
```