import zipfile
import xml.etree.ElementTree as ET

def map_images(docx_path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        # Read relationships
        rels = {}
        for name in docx.namelist():
            if name.endswith('.xml.rels'):
                try:
                    xml_content = docx.read(name)
                    root = ET.fromstring(xml_content)
                    for child in root:
                        rid = child.attrib.get('Id')
                        target = child.attrib.get('Target')
                        rels[f"{name}:{rid}"] = target
                except Exception as e:
                    pass

        # Print all relationships containing media
        print("Media Relationships:")
        for k, v in rels.items():
            if 'media' in v:
                print(f"  {k} -> {v}")

        # Scan document, headers, footers for image references
        for name in docx.namelist():
            if name.endswith('.xml') and not name.startswith('_rels/'):
                try:
                    xml_content = docx.read(name)
                    root = ET.fromstring(xml_content)
                    embeds = root.findall('.//*[@r:embed]', namespaces)
                    if embeds:
                        print(f"\nReferences in {name}:")
                        for embed in embeds:
                            rid = embed.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                            # Look up relationship
                            rel_key_sub = f"{name.replace('word/', 'word/_rels/')}.rels:{rid}"
                            rel_key_main = f"word/_rels/document.xml.rels:{rid}"
                            target = rels.get(rel_key_sub) or rels.get(rel_key_main) or "Unknown"
                            
                            # Try to get surrounding text to give context
                            parent_p = embed
                            p_text = ""
                            for _ in range(10): # go up to 10 levels to find paragraph
                                parent_p = root.find(f".//*[@w:p].../{parent_p.tag}", namespaces) or parent_p
                            
                            # Let's find parent paragraph manually
                            # We'll just print target and parent tag
                            print(f"  Embed rid={rid} -> Target={target} (Tag={embed.tag})")
                except Exception as e:
                    print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    map_images("MR. Mysa Kodaskar_Offer Letter _ SSS (1) 3.docx")
