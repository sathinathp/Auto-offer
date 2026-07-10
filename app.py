import os
import re
from flask import Flask, render_template, request, send_file, jsonify
import weasyprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('output', exist_ok=True)

# Helper function to format currency numbers with commas (Indian Style: 3,60,000)
def format_indian_currency(amount):
    if amount is None or amount == "":
        return ""
    try:
        amount_str = str(amount).replace(",", "")
        if "." in amount_str:
            parts = amount_str.split(".")
            integer_part = parts[0]
            decimal_part = "." + parts[1]
        else:
            integer_part = amount_str
            decimal_part = ""
        n = len(integer_part)
        if n <= 3:
            return integer_part + decimal_part
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        out = []
        while len(remaining) > 2:
            out.append(remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            out.append(remaining)
        out.reverse()
        return ",".join(out) + "," + last_three + decimal_part
    except Exception:
        return amount

@app.template_filter('currency')
def currency_filter(val):
    return format_indian_currency(val)

# ----------------------------------------------------------------
# BLUEBIX form data
# ----------------------------------------------------------------
def get_bluebix_form_data(req_form):
    data = {
        'offer_date':              req_form.get('offer_date') or '26 February 2026',
        'candidate_name':          req_form.get('candidate_name') or 'Bandi Dharani',
        'candidate_prefix':        req_form.get('candidate_prefix') or 'Ms.',
        'mobile_number':           req_form.get('mobile_number') or '+91 8179434324',
        'company_name':            req_form.get('company_name') or 'BLUEBIX SOLUTIONS INC',
        'job_title':               req_form.get('job_title') or 'Recruiter',
        'joining_date':            req_form.get('joining_date') or '16-02-2026',
        'reporting_time':          req_form.get('reporting_time') or '6:00 PM',
        'annual_ctc':              req_form.get('annual_ctc') or '3,60,000',
        'annual_ctc_words':        req_form.get('annual_ctc_words') or 'Three Lakhs Sixty Thousand Indian Rupees',
        'work_shift':              req_form.get('work_shift') or '6:30 PM to 3:30 AM IST',
        'reporting_manager':       req_form.get('reporting_manager') or 'David Felix (Operations Manager)',
        'probation_period':        req_form.get('probation_period') or 'three months (3)',
        'probation_notice_period': req_form.get('probation_notice_period') or '15 days',
        'notice_period':           req_form.get('notice_period') or '30 days',
        'employee_id':             req_form.get('employee_id') or 'BBSHYD0490',
        'department':              req_form.get('department') or 'US Staffing',
        # Salary – monthly
        'basic_monthly':              req_form.get('basic_monthly') or '15,000',
        'hra_monthly':                req_form.get('hra_monthly') or '6,000',
        'conveyance_monthly':         req_form.get('conveyance_monthly') or '6,000',
        'special_allowance_monthly':  req_form.get('special_allowance_monthly') or '3,000',
        'gross_monthly':              req_form.get('gross_monthly') or '30,000',
        'employer_pf_monthly':        req_form.get('employer_pf_monthly') or '0.00',
        'total_a_monthly':            req_form.get('total_a_monthly') or '0',
        'ctc_monthly':                req_form.get('ctc_monthly') or '30,000',
        'employee_pf_monthly':        req_form.get('employee_pf_monthly') or '0.00',
        'professional_tax_monthly':   req_form.get('professional_tax_monthly') or '200',
        'total_b_monthly':            req_form.get('total_b_monthly') or '2,000',
        'total_deductions_monthly':   req_form.get('total_deductions_monthly') or '2,000',
        'net_salary_monthly':         req_form.get('net_salary_monthly') or '28,000',
        # Salary – annual
        'basic_annual':              req_form.get('basic_annual') or '1,80,000',
        'hra_annual':                req_form.get('hra_annual') or '72,000',
        'conveyance_annual':         req_form.get('conveyance_annual') or '72,000',
        'special_allowance_annual':  req_form.get('special_allowance_annual') or '36,000',
        'gross_annual':              req_form.get('gross_annual') or '3,60,000',
        'employer_pf_annual':        req_form.get('employer_pf_annual') or '0',
        'total_a_annual':            req_form.get('total_a_annual') or '0',
        'ctc_annual':                req_form.get('ctc_annual') or '3,60,000',
        'employee_pf_annual':        req_form.get('employee_pf_annual') or '0',
        'professional_tax_annual':   req_form.get('professional_tax_annual') or '2,400',
        'total_b_annual':            req_form.get('total_b_annual') or '24,000',
        'total_deductions_annual':   req_form.get('total_deductions_annual') or '24,000',
        'net_salary_annual':         req_form.get('net_salary_annual') or '3,36,000',
        # Signatories
        'ceo_name': req_form.get('ceo_name') or 'Sanjay Kumar',
        'hr_name':  req_form.get('hr_name') or 'Askani David Raj',
                # Wording text blocks
        'text_intro': req_form.get('text_intro') or f'Subsequent to the discussions that you had with request to your internal movement within the organization, we are pleased to extend an offer of employment to you from <span class="bold">{req_form.get("company_name") or "BLUEBIX SOLUTIONS INC"}</span> as a <span class="bold">{req_form.get("job_title") or "Recruiter"}</span> position. This letter sets out the key terms of the employment. Your responsibilities and duties are detailed in the employment contract.',
        'text_joining': req_form.get('text_joining') or f'Your joining date is <span class="bold">{req_form.get("joining_date") or "16-02-2026"}</span> Please make yourself available at <span class="bold">{req_form.get("reporting_time") or "6:00 PM"}</span> IST in our office on that day. Your <span class="bold">CTC</span> (the cost to the company per annum is <span class="bold">INR {req_form.get("annual_ctc") or "3,60,000"} ({req_form.get("annual_ctc_words") or "Three Lakhs Sixty Thousand Indian Rupees"})</span> take home plus incentive as variable pay. Details are available in the annexure of the employment contract. Your formal appointment letter will be given on the date of your joining. You will be required to sign a <span class="bold">Non-Disclosure Agreement</span> on joining the organization.',
        'text_working_hours': req_form.get('text_working_hours') or f'General working hours for this position are from <span class="bold">{req_form.get("work_shift") or "6:30 PM to 3:30 AM IST"}</span>, Monday to Friday. The office is closed on Saturday& Sunday. However, the candidate should be available on weekends at the company’s request. You may be eligible for receiving compensatory off for those extra hours spent. You would also be required to be flexible to work in the core EST shift on a need basis.',
        'text_probation': req_form.get('text_probation') or f'You will be on probation for <span class="bold">{req_form.get("probation_period") or "three months (3)"}</span> from the date of your joining. Your services will be confirmed after successful completion of three months and <span class="bold">subject to your performance and timely evaluation of your work process. The period of probation can be extended at the discretion of the Management, and you will continue to be on probation till an order of confirmation has been issued in writing.</span>',
        'text_termination_a': req_form.get('text_termination_a') or "Your employment/ services will be governed by Company’s rules and regulations applicable from time to time. If the Company is not satisfied with your performance on any account, the Company reserves the right to terminate your employment with a notice of 15 days or by paying proportionate salary in lieu of any short notice only if you are a confirmed Permanent employee of the organization. This in no way limits the Company’s right to terminate your employment without notice in the event of serious misconduct which include, committing a criminal offence, theft, fraud, embezzlement, intoxication, violence, sexual harassment, damage to the Company’s reputation etc.",
        'text_termination_b': req_form.get('text_termination_b') or "The Company reserves the right to terminate your services without giving any reasons during probation, not giving any kind of compensation or notice as mentioned in point \"a\".",
        'text_contingency': req_form.get('text_contingency') or f"BLUEBIX SOLUTIONS INC is a client Company registered with Petabytz Technologies Pvt. Ltd. You will hereby be receiving any and all official communications from Petabytz Technologies Pvt Ltd.",
        'text_closing': req_form.get('text_closing') or f'We are sure you will have a rewarding and exciting career with {req_form.get("company_name") or "BLUEBIX SOLUTIONS INC"} If you have questions, please do not hesitate to contact us in the signature below. Please send us a signed scan copy of this letter as an acknowledgement of the above offer.',
    }
    # CEO Signature
    sig_ceo_file = request.files.get('sig_ceo_upload')
    if sig_ceo_file and sig_ceo_file.filename != '':
        filename = 'uploaded_sig_ceo' + os.path.splitext(sig_ceo_file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sig_ceo_file.save(filepath)
        data['sig_ceo_path'] = filepath.replace('\\', '/')
    else:
        data['sig_ceo_path'] = req_form.get('sig_ceo_path') or 'static/images/sig_ceo.png'
    # HR Signature
    sig_hr_file = request.files.get('sig_hr_upload')
    if sig_hr_file and sig_hr_file.filename != '':
        filename = 'uploaded_sig_hr' + os.path.splitext(sig_hr_file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sig_hr_file.save(filepath)
        data['sig_hr_path'] = filepath.replace('\\', '/')
    else:
        data['sig_hr_path'] = req_form.get('sig_hr_path') or 'static/images/sig_hr.png'
    return data

# ----------------------------------------------------------------
# PETABYTZ form data
# ----------------------------------------------------------------
def get_petabytz_form_data(req_form):
    data = {
        'offer_date':          req_form.get('pbt_offer_date') or '28-October-2025',
        'candidate_name':      req_form.get('pbt_candidate_name') or 'Gampa Usha',
        'candidate_location':  req_form.get('pbt_candidate_location') or 'Hyderabad, Telangana',
        'mobile_number':       req_form.get('pbt_mobile_number') or '8008809895',
        'job_title':           req_form.get('pbt_job_title') or 'Business Development Executive- IT Sales',
        'joining_date':        req_form.get('pbt_joining_date') or 'Wednesday, 06th October 2025',
        'annual_ctc':          req_form.get('pbt_annual_ctc') or '240,000',
        'annual_ctc_words':    req_form.get('pbt_annual_ctc_words') or 'Two Lakh Forty Thousand Rupees Only',
        'work_shift':          req_form.get('pbt_work_shift') or '09:00 AM to 06:00 PM',
        'probation_period':    req_form.get('pbt_probation_period') or 'three months',
        'notice_period':       req_form.get('pbt_notice_period') or 'two months',
        'employee_id':         req_form.get('pbt_employee_id') or 'PBTHYD0302',
        'department':          req_form.get('pbt_department') or 'Sales & Marketing',
        # Salary – monthly
        'basic_monthly':             req_form.get('pbt_basic_monthly') or '10,000',
        'hra_monthly':               req_form.get('pbt_hra_monthly') or '4,000',
        'lta_monthly':               req_form.get('pbt_lta_monthly') or '2,000',
        'other_allowance_monthly':   req_form.get('pbt_other_allowance_monthly') or '4,000',
        'gross_monthly':             req_form.get('pbt_gross_monthly') or '20,000',
        'employer_pf_monthly':       req_form.get('pbt_employer_pf_monthly') or '0',
        'total_a_monthly':           req_form.get('pbt_total_a_monthly') or '0',
        'ctc_monthly':               req_form.get('pbt_ctc_monthly') or '20,000',
        'employee_pf_monthly':       req_form.get('pbt_employee_pf_monthly') or '0',
        'professional_tax_monthly':  req_form.get('pbt_professional_tax_monthly') or '150',
        'total_b_monthly':           req_form.get('pbt_total_b_monthly') or '150',
        'total_deductions_monthly':  req_form.get('pbt_total_deductions_monthly') or '150',
        'net_salary_monthly':        req_form.get('pbt_net_salary_monthly') or '19,850',
        # Salary – annual
        'basic_annual':             req_form.get('pbt_basic_annual') or '120,000',
        'hra_annual':               req_form.get('pbt_hra_annual') or '48,000',
        'lta_annual':               req_form.get('pbt_lta_annual') or '24,000',
        'other_allowance_annual':   req_form.get('pbt_other_allowance_annual') or '48,000',
        'gross_annual':             req_form.get('pbt_gross_annual') or '240,000',
        'employer_pf_annual':       req_form.get('pbt_employer_pf_annual') or '0',
        'total_a_annual':           req_form.get('pbt_total_a_annual') or '0',
        'ctc_annual':               req_form.get('pbt_ctc_annual') or '240,000',
        'employee_pf_annual':       req_form.get('pbt_employee_pf_annual') or '0',
        'professional_tax_annual':  req_form.get('pbt_professional_tax_annual') or '1,800',
        'total_b_annual':           req_form.get('pbt_total_b_annual') or '1,800',
        'total_deductions_annual':  req_form.get('pbt_total_deductions_annual') or '1,800',
        'net_salary_annual':        req_form.get('pbt_net_salary_annual') or '238,200',
        # Signatory
        'ceo_name': req_form.get('pbt_ceo_name') or 'Sanjay Kumar',
                # Wording text blocks        # Wording text blocks
        'text_intro': req_form.get('sss_text_intro') or f'Subsequent to the discussions that you had with request to your internal movement within the organization, we are pleased to extend an offer of employment to you from <span class="bold">{req_form.get("sss_company_name") or "SOFTSTANDARD SOLUTIONS LLP"}</span> as a <span class="bold">{req_form.get("sss_job_title") or "US HR & Immigration Specialist"}</span> position. This letter sets out the key terms of the employment. Your responsibilities and duties are detailed in the employment contract.',
        'text_joining': req_form.get('sss_text_joining') or f'Your joining date is <span class="bold">{req_form.get("sss_joining_date") or "02 January, 2025"}</span>. Please make yourself available at <span class="bold">{req_form.get("sss_reporting_time") or "7:00 PM"}</span> IST in our office on that day. Your <span class="bold">CTC</span> (the cost to the company per annum is <span class="bold">INR {req_form.get("sss_annual_ctc") or "3,50,000"} ({req_form.get("sss_annual_ctc_words") or "Three Lakhs Sixty Thousand Indian Rupees"})</span> take home plus incentive as variable pay. Details are available in the annexure of the employment contract. Your formal appointment letter will be given on the date of your joining. You will be required to sign a <span class="bold">Non-Disclosure Agreement</span> on joining the organization.',
        'text_working_hours': req_form.get('sss_text_working_hours') or f'General working hours for this position are from <span class="bold">{req_form.get("sss_work_shift") or "7:30 PM to 4:30 AM IST"}</span>, Monday to Friday. The office is closed on Saturday& Sunday. However, the candidate should be available on weekends at the company’s request. You may be eligible for receiving compensatory off for those extra hours spent. You would also be required to be flexible to work in the core EST shift on a need basis.',
        'text_probation': req_form.get('sss_text_probation') or f'You will be on probation period for <span class="bold">{req_form.get("sss_probation_period") or "three months (3)"}</span> from the date of your joining. Your services will be confirmed after successful completion of three months and <span class="bold">subject to your performance and timely evaluation of your work process. The period of probation can be extended at the discretion of the Management, and you will continue to be on probation till an order of confirmation has been issued in writing.</span>',
        'text_termination_a': req_form.get('sss_text_termination_a') or "Your employment/ services will be governed by Company’s rules and regulations applicable from time to time. If the Company is not satisfied with your performance on any account, the Company reserves the right to terminate your employment with a notice of 15 days or by paying proportionate salary in lieu of any short notice only if you are a confirmed Permanent employee of the organization. This in no way limits the Company’s right to terminate your employment without notice in the event of serious misconduct which include, committing a criminal offence, theft, fraud, embezzlement, intoxication, violence, sexual harassment, damage to the Company’s reputation etc.",
        'text_termination_b': req_form.get('sss_text_termination_b') or "The Company reserves the right to terminate your services without giving any reasons during probation, not giving any kind of compensation or notice as mentioned in point \"a\".",
        'text_contingency': req_form.get('sss_text_contingency') or f'SOFTSTANDARD SOLUTIONS LLP is a client Company registered with SOFTSTANDARD SOLUTIONS LLP. You will hereby be receiving any and all official communications from SOFTSTANDARD SOLUTIONS LLP.',
        'text_closing': req_form.get('sss_text_closing') or f'We are sure you will have a rewarding and exciting career with {req_form.get("sss_company_name") or "SOFTSTANDARD SOLUTIONS LLP"}. If you have questions, please do not hesitate to contact us in the signature below. Please send us a signed scan copy of this letter as an acknowledgement of the above offer.',
    }
    # CEO Signature
    sig_ceo_file = request.files.get('pbt_sig_ceo_upload')
    if sig_ceo_file and sig_ceo_file.filename != '':
        filename = 'uploaded_pbt_sig_ceo' + os.path.splitext(sig_ceo_file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sig_ceo_file.save(filepath)
        data['sig_ceo_path'] = filepath.replace('\\', '/')
    else:
        data['sig_ceo_path'] = req_form.get('pbt_sig_ceo_path') or 'static/images/petabytz/img_44.png'
    return data

# ----------------------------------------------------------------
# SOFTSTANDARD form data
# ----------------------------------------------------------------
def get_softstandard_form_data(req_form):
    data = {
        'offer_date':              req_form.get('sss_offer_date') or '20 January 2025',
        'candidate_name':          req_form.get('sss_candidate_name') or 'Voona Sowmith',
        'candidate_prefix':        req_form.get('sss_candidate_prefix') or 'MR.',
        'mobile_number':           req_form.get('sss_mobile_number') or '+91 7095207926',
        'company_name':            req_form.get('sss_company_name') or 'SOFTSTANDARD SOLUTIONS LLP',
        'job_title':               req_form.get('sss_job_title') or 'US HR & Immigration Specialist',
        'joining_date':            req_form.get('sss_joining_date') or '02 January, 2025',
        'reporting_time':          req_form.get('sss_reporting_time') or '7:00 PM',
        'annual_ctc':              req_form.get('sss_annual_ctc') or '3,50,000',
        'annual_ctc_words':        req_form.get('sss_annual_ctc_words') or 'Three Lakhs Fifty Thousand Indian Rupees',
        'work_shift':              req_form.get('sss_work_shift') or '7:30 PM to 4:30 AM IST',
        'reporting_manager':       req_form.get('sss_reporting_manager') or 'Kodaskar Mysa (US Accounts Manager)',
        'probation_period':        req_form.get('sss_probation_period') or 'three months (3)',
        'probation_notice_period': req_form.get('sss_probation_notice_period') or '15 days',
        'notice_period':           req_form.get('sss_notice_period') or '30 days',
        'employee_id':             req_form.get('sss_employee_id') or 'SSSHYD397',
        'department':              req_form.get('sss_department') or 'US Immigration',
        # Salary – monthly
        'basic_monthly':              req_form.get('sss_basic_monthly') or '14,583',
        'hra_monthly':                req_form.get('sss_hra_monthly') or '5,833',
        'conveyance_monthly':         req_form.get('sss_conveyance_monthly') or '5,833',
        'special_allowance_monthly':  req_form.get('sss_special_allowance_monthly') or '2,918',
        'gross_monthly':              req_form.get('sss_gross_monthly') or '29,167',
        'employer_pf_monthly':        req_form.get('sss_employer_pf_monthly') or '0.00',
        'total_a_monthly':            req_form.get('sss_total_a_monthly') or '0',
        'ctc_monthly':                req_form.get('sss_ctc_monthly') or '29,167',
        'employee_pf_monthly':        req_form.get('sss_employee_pf_monthly') or '0.00',
        'professional_tax_monthly':   req_form.get('sss_professional_tax_monthly') or '200',
        'total_b_monthly':            req_form.get('sss_total_b_monthly') or '200',
        'total_deductions_monthly':   req_form.get('sss_total_deductions_monthly') or '200',
        'net_salary_monthly':         req_form.get('sss_net_salary_monthly') or '28,967',
        # Salary – annual
        'basic_annual':              req_form.get('sss_basic_annual') or '1,75,000',
        'hra_annual':                req_form.get('sss_hra_annual') or '70,000',
        'conveyance_annual':         req_form.get('sss_conveyance_annual') or '70,000',
        'special_allowance_annual':  req_form.get('sss_special_allowance_annual') or '35,000',
        'gross_annual':              req_form.get('sss_gross_annual') or '3,50,000',
        'employer_pf_annual':        req_form.get('sss_employer_pf_annual') or '0',
        'total_a_annual':            req_form.get('sss_total_a_annual') or '0',
        'ctc_annual':                req_form.get('sss_ctc_annual') or '3,50,000',
        'employee_pf_annual':        req_form.get('sss_employee_pf_annual') or '0',
        'professional_tax_annual':   req_form.get('sss_professional_tax_annual') or '2,400',
        'total_b_annual':            req_form.get('sss_total_b_annual') or '2,400',
        'total_deductions_annual':   req_form.get('sss_total_deductions_annual') or '2,400',
        'net_salary_annual':         req_form.get('sss_net_salary_annual') or '3,47,600',
        # Signatories
        'ceo_name': req_form.get('sss_ceo_name') or 'Sanjay Kumar',
        'hr_name':  req_form.get('sss_hr_name') or 'Askani David Raj',
                # Wording text blocks
        'text_intro': req_form.get('text_intro') or f'Subsequent to the discussions that you had with request to your internal movement within the organization, we are pleased to extend an offer of employment to you from <span class="bold">{req_form.get("company_name") or "BLUEBIX SOLUTIONS INC"}</span> as a <span class="bold">{req_form.get("job_title") or "Recruiter"}</span> position. This letter sets out the key terms of the employment. Your responsibilities and duties are detailed in the employment contract.',
        'text_joining': req_form.get('text_joining') or f'Your joining date is <span class="bold">{req_form.get("joining_date") or "16-02-2026"}</span> Please make yourself available at <span class="bold">{req_form.get("reporting_time") or "6:00 PM"}</span> IST in our office on that day. Your <span class="bold">CTC</span> (the cost to the company per annum is <span class="bold">INR {req_form.get("annual_ctc") or "3,60,000"} ({req_form.get("annual_ctc_words") or "Three Lakhs Sixty Thousand Indian Rupees"})</span> take home plus incentive as variable pay. Details are available in the annexure of the employment contract. Your formal appointment letter will be given on the date of your joining. You will be required to sign a <span class="bold">Non-Disclosure Agreement</span> on joining the organization.',
        'text_working_hours': req_form.get('text_working_hours') or f'General working hours for this position are from <span class="bold">{req_form.get("work_shift") or "6:30 PM to 3:30 AM IST"}</span>, Monday to Friday. The office is closed on Saturday& Sunday. However, the candidate should be available on weekends at the company’s request. You may be eligible for receiving compensatory off for those extra hours spent. You would also be required to be flexible to work in the core EST shift on a need basis.',
        'text_probation': req_form.get('text_probation') or f'You will be on probation for <span class="bold">{req_form.get("probation_period") or "three months (3)"}</span> from the date of your joining. Your services will be confirmed after successful completion of three months and <span class="bold">subject to your performance and timely evaluation of your work process. The period of probation can be extended at the discretion of the Management, and you will continue to be on probation till an order of confirmation has been issued in writing.</span>',
        'text_termination_a': req_form.get('text_termination_a') or "Your employment/ services will be governed by Company’s rules and regulations applicable from time to time. If the Company is not satisfied with your performance on any account, the Company reserves the right to terminate your employment with a notice of 15 days or by paying proportionate salary in lieu of any short notice only if you are a confirmed Permanent employee of the organization. This in no way limits the Company’s right to terminate your employment without notice in the event of serious misconduct which include, committing a criminal offence, theft, fraud, embezzlement, intoxication, violence, sexual harassment, damage to the Company’s reputation etc.",
        'text_termination_b': req_form.get('text_termination_b') or "The Company reserves the right to terminate your services without giving any reasons during probation, not giving any kind of compensation or notice as mentioned in point \"a\".",
        'text_contingency': req_form.get('text_contingency') or f"BLUEBIX SOLUTIONS INC is a client Company registered with Petabytz Technologies Pvt. Ltd. You will hereby be receiving any and all official communications from Petabytz Technologies Pvt Ltd.",
        'text_closing': req_form.get('text_closing') or f'We are sure you will have a rewarding and exciting career with {req_form.get("company_name") or "BLUEBIX SOLUTIONS INC"} If you have questions, please do not hesitate to contact us in the signature below. Please send us a signed scan copy of this letter as an acknowledgement of the above offer.',
    }
    # CEO Signature
    sig_ceo_file = request.files.get('sss_sig_ceo_upload')
    if sig_ceo_file and sig_ceo_file.filename != '':
        filename = 'uploaded_sss_sig_ceo' + os.path.splitext(sig_ceo_file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sig_ceo_file.save(filepath)
        data['sig_ceo_path'] = filepath.replace('\\', '/')
    else:
        data['sig_ceo_path'] = req_form.get('sss_sig_ceo_path') or 'static/images/softstandard/sig_ceo.png'
    # HR Signature
    sig_hr_file = request.files.get('sss_sig_hr_upload')
    if sig_hr_file and sig_hr_file.filename != '':
        filename = 'uploaded_sss_sig_hr' + os.path.splitext(sig_hr_file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        sig_hr_file.save(filepath)
        data['sig_hr_path'] = filepath.replace('\\', '/')
    else:
        data['sig_hr_path'] = req_form.get('sss_sig_hr_path') or 'static/images/softstandard/sig_hr.png'
    return data

# ----------------------------------------------------------------
# Routes
# ----------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    company = request.form.get('company_template', 'bluebix')
    if company == 'petabytz':
        data = get_petabytz_form_data(request.form)
        data['preview_mode'] = True
        return render_template('offer_letters/petabytz_offer.html', **data)
    elif company == 'softstandard':
        data = get_softstandard_form_data(request.form)
        data['preview_mode'] = True
        return render_template('offer_letters/softstandard_offer.html', **data)
    else:
        data = get_bluebix_form_data(request.form)
        data['preview_mode'] = True
        return render_template('offer_letters/bluebix_offer.html', **data)

@app.route('/generate', methods=['POST'])
def generate():
    company = request.form.get('company_template', 'bluebix')
    if company == 'petabytz':
        data = get_petabytz_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/petabytz_offer.html', **data)
        output_pdf_path = os.path.join('output', f"PetaBytz_Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")
    elif company == 'softstandard':
        data = get_softstandard_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/softstandard_offer.html', **data)
        output_pdf_path = os.path.join('output', f"SoftStandard_Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")
    else:
        data = get_bluebix_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/bluebix_offer.html', **data)
        output_pdf_path = os.path.join('output', f"Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")

    abs_base = os.path.abspath(".")
    weasyprint.HTML(string=html_content, base_url=abs_base).write_pdf(output_pdf_path)
    return send_file(output_pdf_path, as_attachment=True, download_name=os.path.basename(output_pdf_path))

@app.route('/email', methods=['POST'])
def email_offer():
    email_address = request.form.get('email', '')
    company = request.form.get('company_template', 'bluebix')
    
    if company == 'petabytz':
        candidate_name = request.form.get('pbt_candidate_name', 'Candidate')
    elif company == 'softstandard':
        candidate_name = request.form.get('sss_candidate_name', 'Candidate')
    else:
        candidate_name = request.form.get('candidate_name', 'Candidate')
        
    if not email_address:
        return jsonify({'status': 'error', 'message': 'Email address is required.'}), 400

    if company == 'petabytz':
        data = get_petabytz_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/petabytz_offer.html', **data)
        output_pdf_path = os.path.join('output', f"PetaBytz_Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")
    elif company == 'softstandard':
        data = get_softstandard_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/softstandard_offer.html', **data)
        output_pdf_path = os.path.join('output', f"SoftStandard_Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")
    else:
        data = get_bluebix_form_data(request.form)
        data['preview_mode'] = False
        html_content = render_template('offer_letters/bluebix_offer.html', **data)
        output_pdf_path = os.path.join('output', f"Offer_Letter_{data['candidate_name'].replace(' ', '_')}.pdf")

    abs_base = os.path.abspath(".")
    weasyprint.HTML(string=html_content, base_url=abs_base).write_pdf(output_pdf_path)
    print(f"Mocking email delivery to {email_address} with attachment: {output_pdf_path}")
    return jsonify({
        'status': 'success',
        'message': f'Offer Letter successfully emailed to {candidate_name} ({email_address})!'
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
