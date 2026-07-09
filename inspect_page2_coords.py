import fitz
import sys

# Set standard output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

def inspect_page2_coords(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[1] # Page 2
    print("--- Generated PDF Page 2 Text Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for idx, b in enumerate(blocks):
        if b["type"] == 0: # Text block
            for line in b["lines"]:
                for span in line["spans"]:
                    print(f"Text Span: {repr(span['text'])} | bbox={[round(x, 1) for x in span['bbox']]}")
            
if __name__ == "__main__":
    inspect_page2_coords("test_generated.pdf")
