import fitz

doc = fitz.open("output/test_sss.pdf")
with open("new_pages_utf8.txt", "w", encoding="utf-8") as f:
    f.write(f"New PDF total pages: {len(doc)}\n")
    for i, page in enumerate(doc):
        f.write(f"\n================ PAGE {i+1} ================\n")
        text = page.get_text()
        f.write(text.strip() + "\n")
print("Done!")
