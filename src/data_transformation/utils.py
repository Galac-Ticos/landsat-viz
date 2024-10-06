import os
import tarfile
import json
import numpy as np
import cv2
import math
import os


def extract_tar_files(data_directory):
    # List all files in the specified directory
    for filename in os.listdir(data_directory):
        if filename.endswith('.tar'):  # Check for .tar files
            file_path = os.path.join(data_directory, filename)
            print(f'Extracting {filename}...')

            # Open the tar file and extract its contents
            with tarfile.open(file_path, 'r') as tar:
                # Extract to the same directory or specify another
                tar.extractall(path=data_directory)

            print(f'Finished extracting {filename}.\n')


def load_json_files(file_paths):
    json_objects = []

    for file_path in file_paths:
        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    # Load the JSON content
                    json_data = json.load(f)
                    json_objects.append(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

    return json_objects


def find_metadata_json_files(directory_path):
    matching_files = []

    for filename in os.listdir(directory_path):
        # Check if the file ends with 'MTL.json' (case insensitive)
        if filename.lower().endswith("mtl.json"):
            # Construct the full path and add it to the list
            full_path = os.path.join(directory_path, filename)
            matching_files.append(load_json_files([full_path])[0])

    return matching_files
