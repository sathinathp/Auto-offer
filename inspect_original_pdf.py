import fitz

doc = fitz.open("softstandard_original.pdf")
with open("original_coords_utf8.txt", "w", encoding="utf-8") as f:
    f.write(f"Original PDF total pages: {len(doc)}\n")
    for i, page in enumerate(doc):
        f.write(f"\n================ PAGE {i+1} ================\n")
        blocks = page.get_text("blocks")
        for b in sorted(blocks, key=lambda x: (round(x[1], 1), round(x[0], 1))):
            x0, y0, x1, y1, text, block_no, block_type = b
            f.write(f"Block {block_no} (x={x0:.1f}, y={y0:.1f} to {y1:.1f}): {repr(text.strip())}\n")
print("Done!")
