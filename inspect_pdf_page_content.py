import fitz

def inspect_pdf_pages(pdf_path):
    doc = fitz.open(pdf_path)
    for idx, page in enumerate(doc):
        print(f"\n================ ORIGINAL PAGE {idx + 1} =================")
        text = page.get_text()
        print(text)

if __name__ == "__main__":
    inspect_pdf_pages("template_original.pdf")
