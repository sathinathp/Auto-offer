import zipfile
import xml.etree.ElementTree as ET

def inspect_structure(docx_path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        # 1. Read document relationships to map rId to image files
        rels_xml = docx.read('word/_rels/document.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        rid_map = {}
        for child in rels_root:
            rid = child.get('Id')
            target = child.get('Target')
            rid_map[rid] = target
        print("Relationships (rId mapping):")
        for rid, target in rid_map.items():
            if 'media' in target:
                print(f"  {rid} -> {target}")
                
        # 2. Read document body and locate drawing/blip elements
        doc_xml = docx.read('word/document.xml')
        doc_root = ET.fromstring(doc_xml)
        
        # Traverse and find which paragraphs contain images
        p_idx = 0
        for elem in doc_root.iter():
            if elem.tag.endswith('p'):
                p_idx += 1
                # Find blip elements which point to relationships
                blips = elem.findall('.//a:blip', namespaces)
                if blips:
                    p_text = "".join([t.text for t in elem.findall('.//w:t', namespaces) if t.text])
                    print(f"Paragraph {p_idx} (text: '{p_text}') contains images:")
                    for blip in blips:
                        embed_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        print(f"  Embedded Image: rId={embed_rid} -> {rid_map.get(embed_rid, 'Unknown')}")
                        
        # 3. Check header/footer relationships to see if logo or header image is in header/footer
        for filename in docx.namelist():
            if 'header' in filename or 'footer' in filename:
                rels_filename = f"word/_rels/{filename.split('/')[-1]}.rels"
                if rels_filename in docx.namelist():
                    print(f"\nHeader/Footer relations for {filename}:")
                    rels_data = docx.read(rels_filename)
                    rels_root_hf = ET.fromstring(rels_data)
                    hf_rid_map = {}
                    for child in rels_root_hf:
                        hf_rid_map[child.get('Id')] = child.get('Target')
                    
                    hf_xml = docx.read(filename)
                    hf_root = ET.fromstring(hf_xml)
                    blips = hf_root.findall('.//a:blip', namespaces)
                    for blip in blips:
                        embed_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        print(f"  In {filename}: rId={embed_rid} -> {hf_rid_map.get(embed_rid, 'Unknown')}")

if __name__ == "__main__":
    inspect_structure("Edit  - Bluebix Offer letter 2.docx")
