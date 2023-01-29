import os
from PIL import Image, ImageFile

import warnings
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

# Initialize a counter variable
counter = 0

try:
    # Open the watermark image
    watermark = Image.open("watermark.jpg")
except FileNotFoundError:
    watermark = None
    print("Watermark image not found. Images will be saved without watermark.")

ImageFile.LOAD_TRUNCATED_IMAGES = True
# Use os.walk to recursively search for image files
total_files = sum([len(files) for r, d, files in os.walk(".")])
processed_files = 0
for dirpath, dirnames, filenames in os.walk("."):
    for file in filenames:
        if file == os.path.basename(__file__) or file == 'watermark.jpg':
            continue
        # Check if file is an image
        # if file.lower().endswith(("jpg", "jpeg", "png")):
        if file.lower().endswith(("normal.webp")):
            processed_files += 1
            # Construct the full file path by joining the directory path and the file name
            file_path = os.path.join(dirpath, file)
            # Open the image
            with Image.open(file_path) as img:
                # Resize the image to half resolution
                img_half = img.resize(
                    (img.width//5, img.height//5), Image.ANTIALIAS)
                if watermark:
                    # paste the watermark on the image
                    img.paste(watermark, (img.width - watermark.width -
                                          10, img.height - watermark.height - 10), watermark)
                # Save the image with normal resolution
                save_path = os.path.join(os.path.dirname(file_path), os.path.splitext(file)[
                    0] + "_normal.webp")
                # img.save(save_path, "webp", quality=100)
                # # Save the image with half resolution
                save_path = os.path.join(os.path.dirname(file_path), os.path.splitext(file)[
                    0] + "_thumbnail.webp").replace("normal_thumbnail", "thumbnail")
                img_half.save(save_path, "webp", quality=100)
                print(
                    f"{processed_files}/{total_files} - {file} has been converted to {os.path.splitext(file)[0]}_normal.webp and {os.path.splitext(file)[0]}_half.webp")
        else:
            print(f"{file} is not an image.")

# Check if no images were found
if processed_files == 0:
    print("No images found in the current directory and subdirectories. Please check the directory and try again.")
else:
    import winsound
    winsound.Beep(333, 1000)
