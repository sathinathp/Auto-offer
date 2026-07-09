from PIL import Image
import os

assets_dir = "extracted_assets"
for filename in os.listdir(assets_dir):
    if filename.startswith("extracted_image_"):
        path = os.path.join(assets_dir, filename)
        with Image.open(path) as img:
            print(f"Image: {filename}, Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
