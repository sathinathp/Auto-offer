import fitz
import difflib

def clean_text(text):
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    # Replace symbols for comparison
    return text

def compare_pdfs(pdf_orig, pdf_gen):
    doc_orig = fitz.open(pdf_orig)
    doc_gen = fitz.open(pdf_gen)
    
    if len(doc_orig) != len(doc_gen):
        print(f"Warning: Page count mismatch! Original={len(doc_orig)}, Generated={len(doc_gen)}")
        
    for i in range(min(len(doc_orig), len(doc_gen))):
        print(f"\n--- Comparing Page {i+1} ---")
        text_orig = clean_text(doc_orig[i].get_text())
        text_gen = clean_text(doc_gen[i].get_text())
        
        # Remove footer
        footer_orig = "Petabytz Technologies Pvt Ltd I Plot no 201 & 202, Kavuri Hills Rd, Guttala_Begumpet, Kavuri Hills, Hyderabad, 5500033."
        text_orig = text_orig.replace(footer_orig, "").strip()
        text_gen = text_gen.replace(footer_orig, "").strip()
        
        # Replace non-ascii chars to avoid console print issues
        text_orig_safe = text_orig.encode('ascii', errors='replace').decode('ascii')
        text_gen_safe = text_gen.encode('ascii', errors='replace').decode('ascii')
        
        if text_orig_safe == text_gen_safe:
            print("  [OK] Page text matches!")
        else:
            print("  [FAIL] Page text mismatch!")
            # Show diff
            diff = list(difflib.ndiff(text_orig_safe.split(), text_gen_safe.split()))
            added = [d[2:] for d in diff if d.startswith('+ ')]
            removed = [d[2:] for d in diff if d.startswith('- ')]
            if added:
                print(f"    Added in generated: {added[:10]}")
            if removed:
                print(f"    Missing from generated: {removed[:10]}")

if __name__ == "__main__":
    compare_pdfs("template_original.pdf", "test_generated.pdf")
