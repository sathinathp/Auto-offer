import fitz

doc = fitz.open("softstandard_original.pdf")
page = doc[0]

print("Images on Page 1:")
for img in page.get_images(full=True):
    print(img)

print("\nImage Info (rects, etc.):")
for item in page.get_image_info():
    print(item)

print("\nDrawings (first 5):")
draws = page.get_drawings()
for d in draws[:5]:
    print(d)
