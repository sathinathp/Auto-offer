import fitz

def inspect_page_blocks(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    print(f"\n=== Blocks of Page {page_num} in {pdf_path} ===")
    blocks = page.get_text("blocks")
    # Sort blocks by y coordinate (vertical position)
    sorted_blocks = sorted(blocks, key=lambda b: b[1])
    for b_idx, b in enumerate(sorted_blocks):
        x0, y0, x1, y1, text, block_no, block_type = b
        print(f"Block {b_idx}: bbox=({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f}) | Text: {repr(text.strip().replace('\n', ' '))[:80]}")

if __name__ == "__main__":
    inspect_page_blocks("test_generated.pdf", 4)
