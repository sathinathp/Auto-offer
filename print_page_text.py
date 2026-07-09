import fitz

def print_page_text(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    print(f"--- Text of Page {page_num} in {pdf_path} ---")
    print(page.get_text())

if __name__ == "__main__":
    print_page_text("test_generated.pdf", 4)
