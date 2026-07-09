import os
import jinja2
import weasyprint
import fitz

def generate_sss_pdf():
    # Setup Jinja environment
    template_dir = os.path.abspath("templates")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    
    # Custom template filter for currency
    def currency_filter(val):
        # simple mock currency formatter
        return str(val)
    env.filters['currency'] = currency_filter

    # Load template
    template = env.get_template("offer_letters/softstandard_offer.html")
    
    # Mock data similar to get_softstandard_form_data defaults
    context = {
        'offer_date': '20 January 2025',
        'candidate_name': 'Voona Sowmith',
        'candidate_prefix': 'MR.',
        'mobile_number': '+91 7095207926',
        'company_name': 'SOFTSTANDARD SOLUTIONS LLP',
        'job_title': 'US HR & Immigration Specialist',
        'joining_date': '02 January, 2025',
        'reporting_time': '7:00 PM',
        'annual_ctc': '3,50,000',
        'annual_ctc_words': 'Three Lakhs Fifty Thousand Indian Rupees',
        'work_shift': '7:30 PM to 4:30 AM IST',
        'reporting_manager': 'Kodaskar Mysa (US Accounts Manager)',
        'probation_period': 'three months (3)',
        'probation_notice_period': '15 days',
        'notice_period': '30 days',
        'employee_id': 'SSSHYD397',
        'department': 'US Immigration',
        
        # Salary – monthly
        'basic_monthly': '14,583',
        'hra_monthly': '5,833',
        'conveyance_monthly': '5,833',
        'special_allowance_monthly': '2,917',
        'gross_monthly': '29,166',
        'employer_pf_monthly': '0.00',
        'total_a_monthly': '0',
        'ctc_monthly': '29,166',
        'employee_pf_monthly': '0.00',
        'professional_tax_monthly': '200',
        'total_b_monthly': '200',
        'total_deductions_monthly': '200',
        'net_salary_monthly': '28,966',
        
        # Salary – annual
        'basic_annual': '1,75,000',
        'hra_annual': '70,000',
        'conveyance_annual': '70,000',
        'special_allowance_annual': '35,000',
        'gross_annual': '3,50,000',
        'employer_pf_annual': '0',
        'total_a_annual': '0',
        'ctc_annual': '3,50,000',
        'employee_pf_annual': '0',
        'professional_tax_annual': '2,400',
        'total_b_annual': '2,400',
        'total_deductions_annual': '2,400',
        'net_salary_annual': '3,47,600',
        
        # Signatories
        'ceo_name': 'Sanjay Kumar',
        'hr_name': 'Askani David Raj',
        'sig_ceo_path': 'static/images/sig_ceo.png',
        'sig_hr_path': 'static/images/sig_hr.png',
        
        'preview_mode': False
    }
    
    html_content = template.render(context)
    
    os.makedirs("output", exist_ok=True)
    pdf_path = "output/test_sss.pdf"
    
    # Render PDF using WeasyPrint
    print("Generating PDF...")
    weasyprint.HTML(string=html_content, base_url=os.path.abspath(".")).write_pdf(pdf_path)
    print(f"Saved PDF to {pdf_path}")
    
    # Render PDF pages to images using PyMuPDF
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = f"output/test_sss_page{i+1}.png"
        pix.save(img_path)
        print(f"Saved page {i+1} as image to {img_path}")

if __name__ == "__main__":
    generate_sss_pdf()
