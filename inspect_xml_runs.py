import zipfile
import xml.etree.ElementTree as ET

def dump_xml_for_paragraphs(docx_path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        doc_xml = docx.read('word/document.xml')
        root = ET.fromstring(doc_xml)
        body = root.find('.//w:body', namespaces)
        paragraphs = body.findall('.//w:p', namespaces)
        
        target_indices = []
        for idx, p in enumerate(paragraphs):
            p_text = "".join([t.text for t in p.findall('.//w:t', namespaces) if t.text])
            if any(term in p_text for term in ["Sincerely", "Sanjay Kumar", "CEO Founder", "ANNEXURE"]):
                target_indices.append(idx)
                
        for idx in target_indices:
            p = paragraphs[idx]
            p_text = "".join([t.text for t in p.findall('.//w:t', namespaces) if t.text])
            print(f"\n================ Paragraph {idx} (Text: '{p_text}') ================")
            p_xml_str = ET.tostring(p, encoding='utf-8').decode('utf-8')
            # Print first 2000 chars of xml to avoid overflow
            print(p_xml_str[:2000])

if __name__ == "__main__":
    dump_xml_for_paragraphs("Edit  - Bluebix Offer letter 2.docx")
