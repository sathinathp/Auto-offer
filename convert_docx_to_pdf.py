import os
import win32com.client

def convert_to_pdf(docx_path, pdf_path):
    print(f"Converting {docx_path} to {pdf_path}...")
    word = None
    doc = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        # Word needs absolute paths
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        
        doc = word.Documents.Open(abs_docx)
        # wdFormatPDF is 17
        doc.SaveAs(abs_pdf, FileFormat=17)
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")
    finally:
        if doc:
            doc.Close()
        if word:
            word.Quit()

if __name__ == "__main__":
    convert_to_pdf("Edit  - Bluebix Offer letter 2.docx", "template_original.pdf")
