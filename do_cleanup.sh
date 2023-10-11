#!/bin/zsh
# A simple shell script to clean files of certain types from local folders

# Check if the user provided a folder path as an argument
if [ $# -lt 2 ]; then
    echo "Usage: $0 <folder_path> <file_extension1> [<file_extension2> ...]"
    exit 1
else
    echo "Cleanup requested in folder $1"
fi

folder_path="$1"

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: The specified folder does not exist!"
    exit 1
fi

# Shift the first argument to skip the `folder_path`
# and start with the file extensions
shift 1

# Use a loop to process each file extension argument
for ext in "$@"; do
    # Use the find command to locate and remove files with the 
    # specified extension
    find "$folder_path" -type f -name "*.$ext" -exec rm -f {} \;
    echo "Files with '.$ext' extension in $folder_path and its subfolders have been removed."
done