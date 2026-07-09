import fitz

doc = fitz.open("output/test_sss.pdf")
page = doc[0] # page 1
with open("generated_p1_coords.txt", "w", encoding="utf-8") as f:
    f.write("Generated PDF Page 1 Text Blocks with coordinates:\n")
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text, block_no, block_type = b
        f.write(f"Block {block_no} (x={x0:.1f}, y={y0:.1f} to {y1:.1f}): {repr(text.strip())}\n")
print("Done!")
