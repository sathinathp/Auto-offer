import zipfile
import xml.etree.ElementTree as ET

def dump_paragraph_110(docx_path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }
    
    with zipfile.ZipFile(docx_path) as docx:
        doc_xml = docx.read('word/document.xml')
        root = ET.fromstring(doc_xml)
        body = root.find('.//w:body', namespaces)
        paragraphs = body.findall('.//w:p', namespaces)
        
        # Paragraph 110 (which contains the signature drawings)
        p = paragraphs[110]
        p_xml_str = ET.tostring(p, encoding='utf-8').decode('utf-8')
        print(p_xml_str)

if __name__ == "__main__":
    dump_paragraph_110("Edit  - Bluebix Offer letter 2.docx")
