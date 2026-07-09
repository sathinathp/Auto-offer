import fitz

def inspect_page1_coords(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0] # Page 1
    print("--- Generated PDF Page 1 Text Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 0: # Text block
            for line in b["lines"]:
                for span in line["spans"]:
                    print(f"Text Span: '{span['text']}' | bbox={[round(x, 1) for x in span['bbox']]}")
            
if __name__ == "__main__":
    inspect_page1_coords("test_generated.pdf")
