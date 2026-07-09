import fitz

def inspect_page4_coords(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[3] # Page 4
    print(f"--- Generated PDF Page 4 Text Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 0: # Text block
            for line in b["lines"]:
                for span in line["spans"]:
                    print(f"Text Span: '{span['text']}' | bbox={[round(x, 1) for x in span['bbox']]}")
        elif b["type"] == 1: # Image block
            print(f"Image Block: bbox={[round(x, 1) for x in b['bbox']]}")
            
if __name__ == "__main__":
    inspect_page4_coords("test_generated.pdf")
