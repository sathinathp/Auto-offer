import fitz

def inspect_y_positions_safe(pdf_path):
    doc = fitz.open(pdf_path)
    for idx, page in enumerate(doc):
        print(f"\n================ Page {idx + 1} =================")
        blocks = page.get_text("blocks")
        content_blocks = []
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            text_strip = text.strip()
            if not text_strip:
                continue
            if y0 > 800:
                continue
            content_blocks.append((x0, y0, x1, y1, text_strip))
            
        content_blocks.sort(key=lambda x: x[1])
        if content_blocks:
            first = content_blocks[0]
            last = content_blocks[-1]
            # Replace non-ascii chars for safe printing
            first_text_safe = first[4].encode('ascii', errors='replace').decode('ascii')[:60]
            last_text_safe = last[4].encode('ascii', errors='replace').decode('ascii')[:60]
            print(f"First block: bbox=({first[0]:.1f}, {first[1]:.1f}, {first[2]:.1f}, {first[3]:.1f}) | Text: {repr(first_text_safe)}")
            print(f"Last block:  bbox=({last[0]:.1f}, {last[1]:.1f}, {last[2]:.1f}, {last[3]:.1f}) | Text: {repr(last_text_safe)}")
            print(f"Total content blocks: {len(content_blocks)}")
        else:
            print("No content blocks found")

if __name__ == "__main__":
    inspect_y_positions_safe("template_original.pdf")
