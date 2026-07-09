import re

def extract_clean_pages(structure_path, output_path):
    with open(structure_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    pages = re.split(r"--- Page \d+.* ---", content)
    # The first element is before "Page 1"
    pages = [p.strip() for p in pages if p.strip()]
    
    with open(output_path, "w", encoding="utf-8") as out:
        for idx, page_content in enumerate(pages):
            out.write(f"\n================ PAGE {idx + 1} =================\n")
            lines = re.findall(r"Line \d+: '(.*?)' \| Spans:", page_content)
            for line in lines:
                # Remove extra escaped characters if any
                line_clean = line.replace("\\'", "'").replace('\\"', '"')
                out.write(line_clean + "\n")

if __name__ == "__main__":
    extract_clean_pages("pdf_structure.txt", "clean_pages_text.txt")
    print("Done! Clean pages text written to clean_pages_text.txt")
