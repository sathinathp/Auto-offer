import fitz  # PyMuPDF
import sys

def inspect_pdf(pdf_path, output_txt_path):
    doc = fitz.open(pdf_path)
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Total pages: {len(doc)}\n")
        
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            rect = page.rect
            f.write(f"\n--- Page {page_idx + 1} (Size: {rect.width}x{rect.height} pt, approx {rect.width/72:.2f}x{rect.height/72:.2f} inches) ---\n")
            
            drawings = page.get_drawings()
            f.write(f"  Drawings count: {len(drawings)}\n")
            
            images = page.get_images()
            f.write(f"  Images count: {len(images)}\n")
            for img in images:
                f.write(f"    Image: xref={img[0]}, width={img[2]}, height={img[3]}, colorspace={img[5]}\n")
                
            blocks = page.get_text("dict")["blocks"]
            text_blocks_count = sum(1 for b in blocks if b["type"] == 0)
            image_blocks_count = sum(1 for b in blocks if b["type"] == 1)
            f.write(f"  Text blocks: {text_blocks_count}, Image blocks: {image_blocks_count}\n")
            
            # Write all lines and character formatting info
            f.write("  Text lines:\n")
            line_count = 0
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        line_text = ""
                        spans_info = []
                        for span in line["spans"]:
                            line_text += span["text"]
                            spans_info.append(f"({span['text']} [Font:{span['font']} Size:{span['size']:.1f} Color:{span['color']} BBox:{[round(x, 1) for x in span['bbox']]}])")
                        line_count += 1
                        f.write(f"    Line {line_count}: '{line_text}' | Spans: {' '.join(spans_info)}\n")
            
            # Print page footer area (y > 750)
            f.write("  Footer area text:\n")
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["bbox"][3] > 750:
                                f.write(f"    {span['text']} (y={span['bbox'][3]:.1f})\n")

if __name__ == "__main__":
    inspect_pdf("template_original.pdf", "pdf_structure.txt")
    print("Done! Results written to pdf_structure.txt")
