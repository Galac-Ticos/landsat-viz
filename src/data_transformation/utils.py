import os
import tarfile


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


def find_metadata_json_files(directory_path):
    # List to hold the matching file paths
    matching_files = []

    # Loop through all files in the specified directory
    for filename in os.listdir(directory_path):
        # Check if the file ends with 'MTL.Json'
        if filename.endswith("MTL.Json"):
            # Construct the full path and add it to the list
            full_path = os.path.join(directory_path, filename)
            matching_files.append(full_path)

    return matching_files
