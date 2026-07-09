import fitz

def inspect_y_positions(pdf_path):
    doc = fitz.open(pdf_path)
    for idx, page in enumerate(doc):
        print(f"\n================ Page {idx + 1} =================")
        # Sort blocks by vertical coordinate
        blocks = page.get_text("blocks")
        # filter out header (y < 70) and footer (y > 800)
        content_blocks = []
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            text_strip = text.strip()
            if not text_strip:
                continue
            # Check if it's footer
            if y0 > 800:
                continue
            # Check if it's header (none of the text blocks are header except logo images, but let's check)
            content_blocks.append((y0, y1, text_strip))
            
        content_blocks.sort(key=lambda x: x[0])
        if content_blocks:
            first = content_blocks[0]
            last = content_blocks[-1]
            print(f"First block: y0={first[0]:.1f}, y1={first[1]:.1f} | Text: {repr(first[2][:60])}")
            print(f"Last block:  y0={last[0]:.1f}, y1={last[1]:.1f} | Text: {repr(last[2][:60])}")
            print(f"Total content blocks: {len(content_blocks)}")
        else:
            print("No content blocks found")

if __name__ == "__main__":
    inspect_y_positions("template_original.pdf")
