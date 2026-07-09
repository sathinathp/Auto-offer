import zipfile
import os
import xml.etree.ElementTree as ET

def extract_docx_contents(docx_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        # 1. Extract images
        print("Extracting images...")
        img_idx = 1
        for name in docx.namelist():
            if name.startswith('word/media/'):
                ext = name.split('.')[-1]
                out_img_path = os.path.join(out_dir, f"extracted_image_{img_idx}.{ext}")
                with open(out_img_path, 'wb') as img_f:
                    img_f.write(docx.read(name))
                print(f"  Extracted {name} to {out_img_path}")
                img_idx += 1
        
        # 2. Extract and print headers/footers
        print("\nChecking headers/footers...")
        for name in docx.namelist():
            if 'header' in name or 'footer' in name:
                print(f"\n--- Content of {name} ---")
                try:
                    xml_content = docx.read(name)
                    root = ET.fromstring(xml_content)
                    texts = []
                    for elem in root.iter():
                        if elem.tag.endswith('t') and elem.text:
                            texts.append(elem.text)
                    print("".join(texts))
                except Exception as e:
                    print(f"Error reading {name}: {e}")
                    
        # 3. Extract and print tables
        print("\nChecking tables in word/document.xml...")
        doc_xml = docx.read('word/document.xml')
        root = ET.fromstring(doc_xml)
        
        # Helper to get text from an element
        def get_elem_text(element):
            return "".join([t.text for t in element.findall('.//w:t', namespaces) if t.text])
            
        tables = root.findall('.//w:tbl', namespaces)
        print(f"Total tables found in document: {len(tables)}")
        for t_idx, tbl in enumerate(tables):
            print(f"\n--- Table {t_idx + 1} ---")
            rows = tbl.findall('.//w:tr', namespaces)
            for r_idx, row in enumerate(rows):
                cols = row.findall('.//w:tc', namespaces)
                col_texts = [get_elem_text(col) for col in cols]
                print(f"Row {r_idx + 1}: {col_texts}")

        # 4. Extract all paragraphs in order
        print("\nExtracting all paragraphs...")
        body = root.find('.//w:body', namespaces)
        if body is not None:
            with open(os.path.join(out_dir, "extracted_full_body.txt"), "w", encoding="utf-8") as f:
                for elem in body:
                    if elem.tag.endswith('p'):
                        txt = get_elem_text(elem)
                        f.write(f"P: {txt}\n")
                    elif elem.tag.endswith('tbl'):
                        f.write("TBL START\n")
                        rows = elem.findall('.//w:tr', namespaces)
                        for row in rows:
                            cols = row.findall('.//w:tc', namespaces)
                            col_texts = [get_elem_text(col) for col in cols]
                            f.write(f"  ROW: {' | '.join(col_texts)}\n")
                        f.write("TBL END\n")
            print(f"Written full body text to {os.path.join(out_dir, 'extracted_full_body.txt')}")

if __name__ == "__main__":
    extract_docx_contents("MR. Mysa Kodaskar_Offer Letter _ SSS (1) 3.docx", "sss_assets")
