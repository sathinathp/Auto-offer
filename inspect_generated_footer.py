import fitz

def inspect_generated_footer(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    print(f"--- Generated PDF Page 1 (Size: {page.rect.width}x{page.rect.height}) ---")
    
    print("\n--- Drawings (Lines) ---")
    drawings = page.get_drawings()
    for idx, d in enumerate(drawings):
        rect = d["rect"]
        if rect.y0 > 700:
            print(f"Drawing {idx}: type={d['type']}, rect={rect}")
            
    print("\n--- Text blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 0:
            for line in b["lines"]:
                for span in line["spans"]:
                    if span["bbox"][3] > 700:
                        print(f"Text Span: '{span['text']}' | bbox={[round(x, 1) for x in span['bbox']]}")
                        
if __name__ == "__main__":
    inspect_generated_footer("test_generated.pdf")
