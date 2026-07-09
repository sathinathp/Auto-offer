import fitz

def verify_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    print(f"File: {pdf_path}")
    print(f"Total Pages: {len(doc)}")
    for idx, page in enumerate(doc):
        print(f"Page {idx + 1} size: {page.rect.width:.1f}x{page.rect.height:.1f}")
        # Count text blocks and images
        text = page.get_text()
        print(f"  Text length: {len(text)} chars")
        images = page.get_images()
        print(f"  Images count: {len(images)}")
        
if __name__ == "__main__":
    verify_pdf("test_generated.pdf")
