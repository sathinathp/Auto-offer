import fitz

def inspect_drawings(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0] # Page 1
    print("--- Drawings (Lines) on Page 1 ---")
    drawings = page.get_drawings()
    for idx, d in enumerate(drawings):
        # We look for lines in the footer area (y > 750)
        rect = d["rect"]
        if rect.y0 > 750:
            print(f"Drawing {idx}: type={d['type']}, rect={rect}, color={d['color']}, width={d['width']}")
            for item in d["items"]:
                print(f"  item: {item}")
                
    print("\n--- Image blocks on Page 1 ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 1: # Image block
            print(f"Image Block {idx}: bbox={b['bbox']}")
            
if __name__ == "__main__":
    inspect_drawings("template_original.pdf")
