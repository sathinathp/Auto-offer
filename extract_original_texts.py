import fitz

def main():
    doc = fitz.open("Gampa Usha Offer letter (1).pdf")
    with open("petabytz_spans.txt", "w", encoding="utf-8") as f:
        for i, page in enumerate(doc):
            f.write(f"\n=== Page {i+1} Text Spans ===\n")
            blocks = page.get_text("dict")["blocks"]
            span_count = 0
            for b in blocks:
                if b["type"] == 0:  # Text block
                    for line in b["lines"]:
                        for span in line["spans"]:
                            span_count += 1
                            bbox = [round(x, 2) for x in span["bbox"]]
                            color = span["color"]
                            r = (color >> 16) & 255
                            g = (color >> 8) & 255
                            b_val = color & 255
                            hex_color = f"#{r:02x}{g:02x}{b_val:02x}"
                            f.write(f"Span {span_count}: bbox={bbox} font={span['font']} size={round(span['size'], 2)} color={hex_color} text={repr(span['text'])}\n")

if __name__ == "__main__":
    main()
