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


def rotation_angle(A, B):
    x1, y1 = A
    x2, y2 = B
    angle = math.atan2(y2-y1, x2-x1)
    return angle


def rotate_image(image_path: str, angle: float = 10.8):
    img = Image.open(image_path)
    path, extension = os.path.splitext(image_path)
    rotated = f'{path}-r{angle}{extension}'
    img.rotate(angle).save(rotated)
    return rotated


def get_colors(img):
    color_str = []
    quantized = img.quantize(colors=10, kmeans=3)
    convert_rgb = quantized.convert('RGB')
    colors = convert_rgb.getcolors()
    color_str = sorted(colors, reverse=True)
    final_list = []
    for i in color_str:
        final_list.append(i[1])
    return final_list[0]


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


def color_map(image_path: str):
    img = Image.open(image_path)
    w, _ = img.size
    k = 3
    s = w // k
    points = [i*(w//k) for i in range(k)]
    boxes = [[(points[i], points[j], points[i] + s, points[j] + s) for i in range(k)] for j in range(k)]
    cmap = [[get_colors(img.crop(boxes[i][j])) for j in range(k)] for i in range(k)]
    return cmap
    

def rotate_and_save_image(image_path: str):
    angle = get_angle_of_rotation(
        '/home/alexbrenes/git/landsat-viz/src/data/LC09_L1TP_015053_20240801_20240802_02_T1_thumb_large.jpeg')
    return rotate_image(image_path, angle)

rotated = rotate_and_save_image('/home/alexbrenes/git/landsat-viz/src/data/LC09_L1TP_015053_20240801_20240802_02_T1_thumb_large.jpeg')
print(color_map(rotated))

# rotate_and_save_image(
#     '/home/alexbrenes/git/landsat-viz/src/data/LC09_L1TP_015053_20240801_20240802_02_T1_thumb_large.jpeg')
