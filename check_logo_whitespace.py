from PIL import Image

img = Image.open("static/images/softstandard/logo.jpg").convert("L")
width, height = img.size

# Find first non-white pixel from top, bottom, left, right
# Let's define threshold for "non-white" (e.g. < 240)
threshold = 240

top = height
bottom = 0
left = width
right = 0

for y in range(height):
    for x in range(width):
        pixel = img.getpixel((x, y))
        if pixel < threshold:
            if y < top: top = y
            if y > bottom: bottom = y
            if x < left: left = x
            if x > right: right = x

print(f"Image Size: {img.size}")
print(f"Non-white BBox: left={left}, top={top}, right={right}, bottom={bottom}")
print(f"Top margin: {top}px")
print(f"Bottom margin: {height - 1 - bottom}px")
print(f"Left margin: {left}px")
print(f"Right margin: {width - 1 - right}px")
print(f"Trimmed size: {right - left + 1}x{bottom - top + 1}")
