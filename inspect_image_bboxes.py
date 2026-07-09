import fitz

def inspect_image_bboxes(pdf_path):
    doc = fitz.open(pdf_path)
    for idx, page in enumerate(doc):
        print(f"\n--- Page {idx + 1} ---")
        image_info = page.get_image_info(rects=True)
        for img in image_info:
            print(f"  Image: xref={img.get('xref')}, bbox={img.get('bbox')}, width={img.get('width')}, height={img.get('height')}")

if __name__ == "__main__":
    inspect_image_bboxes("softstandard_original.pdf")
