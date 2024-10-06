import json
import os
from datetime import datetime
from shapely.geometry import mapping, Polygon
import tarfile

def serialize_polygon(polygon):
    """Convert a Polygon object to a GeoJSON-like dictionary."""
    return mapping(polygon)


def serialize_scene(scene):
    """Convert scene data into a JSON-serializable format."""
    serialized_scene = {}

    for key, value in scene.items():
        if isinstance(value, datetime):
            # Convert datetime to ISO format
            serialized_scene[key] = value.isoformat()
        elif isinstance(value, Polygon):
            serialized_scene[key] = serialize_polygon(
                value)  # Convert Polygon to GeoJSON-like dict
        elif isinstance(value, list):  # Check if the value is a list
            serialized_scene[key] = [v.isoformat() if isinstance(
                v, datetime) else v for v in value]
        else:
            serialized_scene[key] = value  # Keep other values as is

    return serialized_scene


def write_scene_json(scene):
    # Create the 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Serialize the scene to a JSON-compatible format
    serialized_scene = serialize_scene(scene)

    display_id = serialized_scene['display_id']
    filename = os.path.join('data', f"{display_id}.json")

    # Write the serialized scene data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(serialized_scene, json_file, indent=4)


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
