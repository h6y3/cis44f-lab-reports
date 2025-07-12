#!/bin/bash

echo "Lab Structure Creator"
echo "====================="

read -p "Enter lab number (e.g., 1, 6a, 6b): " lab_number
read -p "Enter number of tasks: " task_count

if [[ -z "$lab_number" || -z "$task_count" ]]; then
    echo "Error: Both lab number and task count are required."
    exit 1
fi

if ! [[ "$task_count" =~ ^[0-9]+$ ]] || [ "$task_count" -le 0 ]; then
    echo "Error: Task count must be a positive integer."
    exit 1
fi

lab_folder="Lab${lab_number}"

echo "Creating folder structure for $lab_folder with $task_count tasks..."

mkdir -p "$lab_folder"

for ((i=1; i<=task_count; i++)); do
    task_folder="$lab_folder/task $i"
    mkdir -p "$task_folder"
    echo "Created: $task_folder"
done

echo "Successfully created lab structure for $lab_folder with $task_count tasks."