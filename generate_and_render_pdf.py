import requests
import os
import fitz

def generate_and_render():
    url = "http://127.0.0.1:5000/generate"
    data = {
        'company_template': 'petabytz',
        'pbt_offer_date': '19-March-2025',
        'pbt_candidate_name': 'Sathinath Padhi',
        'pbt_candidate_location': 'Hyderabad, Telangana',
        'pbt_mobile_number': '7787981402',
        'pbt_job_title': 'Business Development Executive- IT Sales',
        'pbt_joining_date': 'Wednesday, 06th October 2025',
        'pbt_annual_ctc': '3,00,000',
        'pbt_annual_ctc_words': 'Three Lakh Indian Rupees',
        'pbt_work_shift': '09:00 AM to 06:00 PM',
        'pbt_probation_period': 'three months',
        'pbt_notice_period': 'two months',
        'pbt_employee_id': 'PBTHYD0302',
        'pbt_department': 'Sales & Marketing',
        'pbt_ceo_name': 'Sanjay Kumar'
    }

    print("Requesting PDF generation...")
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        print(r.text)
        return

    os.makedirs("output", exist_ok=True)
    pdf_path = "output/test_pbt.pdf"
    with open(pdf_path, "wb") as f:
        f.write(r.content)
    print(f"Saved PDF to {pdf_path}")

    # Render PDF pages to images using PyMuPDF
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = f"output/test_pbt_page{i+1}.png"
        pix.save(img_path)
        print(f"Saved page {i+1} as image to {img_path}")

if __name__ == "__main__":
    generate_and_render()
