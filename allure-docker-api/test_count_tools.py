import os
import re

def count_matching_files(directory, search_string, logger):
    match_count = 0
    pattern = re.compile(re.escape(search_string))  # Compile regex for efficient searching

    if logger is not None:
        logger.info("dir " + directory)

    for root, _, files in os.walk(directory):  # Walk through all files in the directory
        for file in files:
            logger.info("file " + file)
            
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if any(pattern.search(line) for line in f):  # Check if any line contains the string
                        match_count += 1
            except Exception as e:
                print(f"Skipping {file_path}: {e}")  # Handle errors like permission issues

def count_passed_result_files(results_dir, logger):
    return count_matching_files(results_dir, '\"status\": \"passed\"', logger)

def count_failed_result_files(results_dir):
    return count_matching_files(results_dir, '\"status\": \"failed\"')

def count_skipped_result_files(results_dir):
    return count_matching_files(results_dir, '\"status\": \"skipped\"')

def count_total_result_files(results_dir):
    return [f for f in os.listdir(results_dir) if '-result.json' in f]

def read_count_from_file(file_path):
    with open(file_path, 'r') as f:
        return int(f.read().strip())
