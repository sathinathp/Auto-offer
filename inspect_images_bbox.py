import fitz

def inspect_images_bbox(pdf_path):
    doc = fitz.open(pdf_path)
    for idx, page in enumerate(doc):
        print(f"\n--- Page {idx + 1} ---")
        blocks = page.get_text("dict")["blocks"]
        for b_idx, block in enumerate(blocks):
            if block["type"] == 1:  # Image block
                bbox = block["bbox"]
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                print(f"  Image Block {b_idx}: bbox={bbox}, width={w:.1f}, height={h:.1f}")
                
        # Also let's find the drawing paths (like borders/lines in headers or tables)
        drawings = page.get_drawings()
        print(f"  Drawings count: {len(drawings)}")
        for d_idx, draw in enumerate(drawings[:5]):
            print(f"    Drawing {d_idx}: type={draw['type']}, rect={draw['rect']}")
            
if __name__ == "__main__":
    inspect_images_bbox("template_original.pdf")
