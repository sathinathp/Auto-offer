import fitz

def inspect_page4_images(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[3] # Page 4 (0-indexed)
    print("--- Page 4 Image Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 1: # Image block
            print(f"Image Block {idx}: bbox={[round(x, 1) for x in b['bbox']]}")
            
    print("\n--- Page 4 Drawings ---")
    drawings = page.get_drawings()
    for idx, d in enumerate(drawings):
        rect = d["rect"]
        if rect.y0 > 600:
            print(f"Drawing {idx}: rect={[round(x, 1) for x in [rect.x0, rect.y0, rect.x1, rect.y1]]}")
            
if __name__ == "__main__":
    inspect_page4_images("template_original.pdf")
