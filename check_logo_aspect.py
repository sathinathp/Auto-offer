from PIL import Image

img = Image.open("static/images/softstandard/logo.jpg")
print(f"Logo dimensions: {img.size}")
print(f"Aspect ratio: {img.size[0] / img.size[1]}")
