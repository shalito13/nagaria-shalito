import os
import re
import subprocess

from PIL import Image


def get_resolution(filename):
    match = re.match(r"(.*)_(\d+)x(\d+)\.(.*)", filename)
    if match:
        return int(match.group(2)), int(match.group(3))
    else:
        with Image.open(filename) as im:
            return im.size


def generate_resolution(filename, resolution, format):
    with Image.open(filename) as im:
        im.resize((resolution, resolution * im.height // im.width)).save(
            f"{filename[:-4]}_{resolution}x{resolution * im.height // im.width}.{format}")


def process_image(filename):
    resolution_1x = 320
    resolution_2x = 750
    resolution_3x = 2048

    format = filename.split(".")[-1].lower()
    if format not in ["jpg", "jpeg", "png", "webp"]:
        return

    width, height = get_resolution(filename)
    if width <= resolution_1x:
        return

    generate_resolution(filename, resolution_1x, format)
    generate_resolution(filename, resolution_2x, format)
    generate_resolution(filename, resolution_3x, format)

    if format != "webp":
        subprocess.call(
            ["cwebp", "-q", "70", f"{filename}", "-o", f"{filename[:-4]}.webp"])


def process_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            process_image(os.path.join(root, file))


process_folder(
    "D:/Development/nagaria/nagaria-src/nagaria-shalito-src/src/assets/img/wood-patterns")
