import os
import tarfile
from PIL import Image, ImageDraw
from colorthief import ColorThief
import math
import cv2
import numpy as np


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


def rotation_angle(A, B):
    x1, y1 = A
    x2, y2 = B
    angle = math.atan2(y2-y1, x2-x1)
    return angle


def rotate_image(image_path: str, angle: float = 10.8):
    img = Image.open(image_path)
    path, extension = os.path.splitext(image_path)
    img.rotate(angle).save(f'{path}-r{angle}{extension}')


def get_colors(image_path: str):
    color_str = []
    img = Image.open(image_path)
    width, height = img.size
    quantized = img.quantize(colors=10, kmeans=3)
    convert_rgb = quantized.convert('RGB')
    colors = convert_rgb.getcolors()
    color_str = sorted(colors, reverse=True)
    final_list = []
    for i in color_str:
        final_list.append(i[1])
    print(final_list[0])  # TODO: CHANGE TO RETURN


def highlight(image_path: str, A, B, C, D, color="magenta"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.line([A, B], fill=80)
    draw.line([A, C], fill=50)
    draw.line([B, D], fill=128)
    draw.line([C, D], fill=200)
    path, extension = os.path.splitext(image_path)
    img.save(f'{path}-drwn{extension}')


def get_angle_of_rotation(path):
    # Finding image
    img_path = path

    # Reading image and converting to gray scale
    img_before = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    img_gray[img_gray > 0] = 255
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0,
                            100, minLineLength=20, maxLineGap=5)

    # Finding angles using slope formula tan(θ) = (y2-y1)/(x2-x1)
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # The algorithm will detect multiple lines and edges. We take the median of all angles
    median_angle = np.median(angles)+90

    return median_angle


def rotate_and_save_image(image_path: str):
    angle = get_angle_of_rotation(image_path)
    rotate_image(image_path, angle)
