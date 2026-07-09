import zipfile
import xml.etree.ElementTree as ET

def inspect_signatures(docx_path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        doc_xml = docx.read('word/document.xml')
        root = ET.fromstring(doc_xml)
        
        # Let's find paragraphs near "Sincerely Yours"
        body = root.find('.//w:body', namespaces)
        paragraphs = body.findall('.//w:p', namespaces)
        
        start_printing = False
        count = 0
        for idx, p in enumerate(paragraphs):
            p_text = "".join([t.text for t in p.findall('.//w:t', namespaces) if t.text])
            if "Sincerely" in p_text:
                start_printing = True
            if start_printing:
                count += 1
                print(f"\n--- Paragraph {idx} (Text: '{p_text}') ---")
                for child in p:
                    # Print XML structure of runs
                    if child.tag.endswith('r'):
                        r_text = "".join([t.text for t in child.findall('.//w:t', namespaces) if t.text])
                        has_drawing = child.find('.//w:drawing', namespaces) is not None
                        print(f"  Run: text='{r_text}', has_drawing={has_drawing}")
                        if has_drawing:
                            blips = child.findall('.//a:blip', namespaces)
                            for blip in blips:
                                embed_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                print(f"    Drawing blip embed={embed_rid}")
                if count > 15:
                    break

if __name__ == "__main__":
    inspect_signatures("Edit  - Bluebix Offer letter 2.docx")
