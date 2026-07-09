import os
import base64
from datetime import datetime
from weasyprint import HTML


class PetaBytzOfferLetterGenerator:
    """
    Generates a PetaBytz Technology Services offer letter PDF
    that exactly matches the design of 'Gampa Usha Offer letter (1).pdf'.
    4 pages: Intro+Terms | Terms cont. | Declaration | Annexure
    """

    def __init__(self, output_dir="media/offer_letters"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.base_dir   = os.path.abspath(".")
        # Logo extracted from original PDF (page 1, xref=7)
        self.logo_path  = os.path.join(self.base_dir, "static", "images", "petabytz", "img_7.png")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _b64(self, path):
        try:
            with open(path, "rb") as fh:
                return base64.b64encode(fh.read()).decode("utf-8")
        except Exception:
            return ""

    def _fmt(self, n):
        """Indian number format: 2,40,000"""
        s = str(abs(int(round(n))))
        if len(s) <= 3:
            return s
        last3 = s[-3:]
        rest  = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        return ",".join(groups) + "," + last3

    def _number_to_words(self, num: int) -> str:
        ones  = ["", "One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
        teens = ["Ten","Eleven","Twelve","Thirteen","Fourteen","Fifteen",
                 "Sixteen","Seventeen","Eighteen","Nineteen"]
        tens_ = ["","","Twenty","Thirty","Forty","Fifty",
                 "Sixty","Seventy","Eighty","Ninety"]

        def b1000(n):
            if n == 0:  return ""
            if n < 10:  return ones[n]
            if n < 20:  return teens[n - 10]
            if n < 100: return tens_[n//10] + (" " + ones[n%10] if n%10 else "")
            return ones[n//100] + " Hundred" + (" " + b1000(n%100) if n%100 else "")

        if num == 0: return "Zero"
        cr = num // 10000000; num %= 10000000
        lk = num // 100000;   num %= 100000
        th = num // 1000;     num %= 1000
        parts = []
        if cr: parts.append(b1000(cr) + " Crore")
        if lk: parts.append(b1000(lk) + " Lakh")
        if th: parts.append(b1000(th) + " Thousand")
        if num: parts.append(b1000(num))
        return " ".join(parts) + " Rupees Only"

    def _salary(self, annual_ctc):
        """PetaBytz split: Basic 50%, HRA 20%, LTA 10%, Other 20%."""
        mg   = annual_ctc / 12
        bsc  = round(mg * 0.50)
        hra  = round(mg * 0.20)
        lta  = round(mg * 0.10)
        oth  = round(mg) - bsc - hra - lta
        pt   = 150
        net  = round(mg) - pt
        m = dict(basic=bsc, hra=hra, lta=lta, other=oth,
                 gross=round(mg), emp_pf=0, total_a=0, ctc=round(mg),
                 ePF=0, pt=pt, total_b=pt, deductions=pt, net=net)
        a = {k: (v * 12 if k != "gross" and k != "ctc" else round(annual_ctc))
             for k, v in m.items()}
        a["gross"] = round(annual_ctc)
        a["ctc"]   = round(annual_ctc)
        return m, a

    # ------------------------------------------------------------------
    # HTML builder
    # ------------------------------------------------------------------
    def _html(self, d):
        logo_b64 = self._b64(self.logo_path)
        m, a = self._salary(float(d.get("annual_ctc", 0)))

        # CEO signature
        sig_ceo = ""
        if d.get("ceo_sig_b64"):
            sig_ceo = f'<img src="data:image/png;base64,{d["ceo_sig_b64"]}" style="max-height:45pt;max-width:110pt;display:block;margin-bottom:3pt;">'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
/* ── Page setup ─────────────────────────────────────── */
@page {{
    size: A4;               /* 595.28pt × 841.89pt */
    margin: 118pt 39pt 48pt 39pt;

    @top-left {{
        content: element(pbt-header);
        vertical-align: top;
    }}
    @bottom-center {{
        content: element(pbt-footer);
        vertical-align: bottom;
    }}
}}

/* ── Running header (every page) ────────────────────── */
#pbt-header {{
    position: running(pbt-header);
    width: 100%;
    margin: 0; padding: 0;
}}
.hdr-topbar {{
    display: block;
    width: 100%;
    height: 8pt;
    background: linear-gradient(90deg, #12305a 0%, #1e5799 50%, #12305a 100%);
}}
.hdr-logo {{
    display: block;
    height: 42pt;
    width: auto;
    margin: 10pt 0 0 18pt;
}}

/* ── Running footer (every page) ────────────────────── */
#pbt-footer {{
    position: running(pbt-footer);
    width: 100%;
    background: linear-gradient(90deg, #12305a 0%, #1e5799 50%, #12305a 100%);
    display: table;
    table-layout: fixed;
    padding: 7pt 14pt;
    box-sizing: border-box;
}}
.ftr-left {{
    display: table-cell;
    color: #ffffff;
    font-family: 'Times New Roman', Times, serif;
    font-size: 9pt;
    vertical-align: middle;
    white-space: nowrap;
}}
.ftr-right {{
    display: table-cell;
    color: #ffffff;
    font-family: 'Times New Roman', Times, serif;
    font-size: 9pt;
    vertical-align: middle;
    text-align: right;
    white-space: nowrap;
}}

/* ── Body ───────────────────────────────────────────── */
body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11.6pt;
    line-height: 1.22;
    color: #000000;
    text-align: justify;
    margin: 0; padding: 0;
}}
p {{ margin: 0 0 9pt 0; }}

.bold   {{ font-weight: bold; }}
.center {{ text-align: center; }}

/* PRIVATE AND CONFIDENTIAL */
.pc-head      {{ font-size: 13pt; font-weight: bold; margin-bottom: 20pt; }}
.pc-green     {{ color: #365C11; }}
.pc-blue      {{ color: #1F407A; }}

/* Candidate meta block */
.meta-block   {{ margin-bottom: 12pt; line-height: 1.45; }}
.meta-block p {{ margin-bottom: 0; text-align: left; }}

/* Section headings */
.h-blue {{
    font-size: 12pt; font-weight: bold;
    color: #1F407A; text-align: center;
    margin: 10pt 0 8pt 0;
}}
.h-teal {{
    font-size: 12pt; font-weight: bold;
    color: #4F807A;
    margin: 14pt 0 5pt 0;
}}

/* Page breaks */
.pb {{ page-break-before: always; }}

/* Annexure */
.ann-title {{
    font-size: 13pt; font-weight: bold;
    color: #1F407A; text-align: center;
    margin: 0 0 8pt 0;
}}
.ann-sub {{
    font-size: 11.6pt; font-weight: bold;
    text-align: center; margin: 5pt 0 4pt 0;
}}
table.info-tbl {{
    width: 100%; border-collapse: collapse;
    margin-bottom: 5pt; font-size: 11.6pt;
}}
table.info-tbl td {{
    border: 0.5pt solid #000;
    padding: 3pt 7pt;
    vertical-align: middle;
}}
table.info-tbl .lbl {{ font-weight: bold; width: 40%; }}

table.sal-tbl {{
    width: 100%; border-collapse: collapse;
    font-size: 11.6pt;
}}
table.sal-tbl td {{
    border: 0.5pt solid #000;
    padding: 3pt 7pt;
    vertical-align: middle;
}}
table.sal-tbl .r {{ text-align: right; }}
table.sal-tbl .hdr td {{
    font-weight: bold;
    background: #f0f0f0;
    text-align: center;
}}
table.sal-tbl .bld td {{ font-weight: bold; }}
table.sal-tbl .hl  td {{
    font-weight: bold;
    background: #dce6f1;
}}
.note-text {{ font-size: 11pt; margin-top: 5pt; }}

/* Signature section */
.sig-block {{ margin-top: 16pt; }}
.sig-grid  {{ display: table; width: 100%; }}
.sig-l     {{ display: table-cell; width: 50%; vertical-align: top; }}
.sig-r     {{ display: table-cell; width: 50%; vertical-align: bottom;
              text-align: right; padding-top: 20pt; }}
</style>
</head>
<body>

<!-- RUNNING HEADER -->
<div id="pbt-header">
  <div class="hdr-topbar"></div>
  <img class="hdr-logo" src="data:image/png;base64,{logo_b64}" alt="PetaBytz Logo">
</div>

<!-- RUNNING FOOTER -->
<div id="pbt-footer">
  <div class="ftr-left">+91-89779 15322(Ind)</div>
  <div class="ftr-right">1st Floor I DMR Corporate I Kavuri Hills I Madhapur I HYD – 500033</div>
</div>

<!-- ═══════════════════════════════════════════ PAGE 1 ═══ -->
<p class="pc-head">
  <span class="pc-green">PRIVATE AND </span><span class="pc-blue">CONFIDENTIAL</span>
</p>

<div class="meta-block">
  <p>Date: <strong>{d.get('date','28-October-2025')}</strong></p>
  <p>Name: <strong>{d.get('name','')}</strong></p>
  <p>Location: {d.get('location','Hyderabad, Telangana')}</p>
  <p>Contact: (M) – {d.get('contact','')}</p>
</div>

<p>&nbsp;</p>
<p>Subject: Employment Appointment Letter</p>
<p>Dear {d.get('name','')},</p>

<p>We are pleased to extend an offer of employment to you for the position of <strong>{d.get('designation','')}</strong> at <strong>PetaBytz Technology Services Private Limited</strong>. This letter outlines the key terms of your employment.</p>

<p><strong>Joining Date: {d.get('joining_date','')}</strong></p>
<p>&nbsp;</p>
<p><strong>Annual CTC: ₹ {self._fmt(d.get('annual_ctc',0))} ({d.get('annual_ctc_words','')})</strong></p>
<p>&nbsp;</p>

<p>The general terms and conditions governing your employment, compensation, and other benefits are detailed in the enclosed document. We look forward to having you as part of our team and are confident that you will have a successful and rewarding career with our company.</p>

<div class="h-blue">General Terms and Conditions of Employment</div>

<p><strong>Base Location:</strong> Your base location will be Hyderabad, DMR Corporate, Kavuri Hills, Madhapur. However, during your employment, you may be posted or transferred to any of the company's offices, projects, divisions, departments, units, or clients at any location in India or abroad, as applicable.</p>

<p><strong>Working Hours:</strong> The general working hours for this position are from {d.get('work_shift','09:00 AM to 06:00 PM')} IST (Should also be flexible to work at any time as per the client's needs), Monday to Friday. Flexibility to work outside these hours may be required. The office is closed on Saturdays and Sundays, but you may be required to be available on weekends upon the company's request. Compensatory off may be provided for extra hours worked.</p>

<p><strong>Probation:</strong> You will be on probation for {d.get('probation_period','three months')} from your joining date. Your services will be confirmed after the successful completion of the probation period, subject to performance evaluation. The probation period may be extended at the management's discretion, and you will remain on probation until a written confirmation is issued.</p>

<p><strong>Notice and Termination:</strong> The notice period is {d.get('notice_period','two months')}. During the probation period, your services may be terminated at any time without notice, pay, or advance intimation. Reasons for termination include, but are not limited to, theft, harassment, absconding from duties, inaccessibility during office working hours, frequent leaves, and low productivity.</p>

<!-- ═══════════════════════════════════════════ PAGE 2 ═══ -->
<div class="pb"></div>

<p>&nbsp;</p>
<p>After successful completion of the probation period, your services may be terminated by giving two weeks' notice or two weeks' salary in lieu thereof. Upon termination of employment, you are required to immediately hand over to the Company all correspondence, specifications, formulae, books, documents, market data, cost data, drawings, effects, or records belonging to the Company or relating to its business. You shall not retain or make copies of these items. Additionally, you must return all company property in your possession upon termination of employment.</p>

<p>Please note that salary information is confidential and should not be discussed with colleagues or within the Company. Breaching this policy will be considered a violation of Company Policy.</p>

<div class="h-teal">Performance Appraisal</div>

<p>Your performance will be continuously monitored throughout your tenure with PetaBytz Technology Services Private Limited. A formal performance appraisal will be conducted during the standard appraisal cycle, which typically occurs annually.</p>

<p>The performance appraisal process involves evaluating your job performance against predefined goals and objectives. This evaluation will consider various factors, such as your job knowledge, quality of work, productivity, teamwork, communication skills, and adherence to company policies and procedures.</p>

<p>During the appraisal process, you will have an opportunity to discuss your achievements, challenges, and career aspirations with your manager. Constructive feedback will be provided to help you improve your performance and achieve your professional goals.</p>

<p>Based on the results of the performance appraisal, decisions regarding salary adjustments, promotions, bonuses, and other rewards will be made. It is important to actively participate in the appraisal process and work towards continuous improvement.</p>

<div class="h-teal">Confidentiality and Data Protection</div>

<p>As an employee of PetaBytz Technology Services Private Limited, you will have access to confidential information that is essential to our business operations. This information includes but is not limited to trade secrets, proprietary data, customer lists, financial information, marketing strategies, product development plans, and other sensitive information.</p>

<p>You are required to maintain the confidentiality of all such information during and after your employment with the company. You must not disclose any confidential information to any third party without prior written consent from the company. Additionally, you must take all necessary precautions to protect the confidentiality of this information and prevent unauthorized access or disclosure.</p>

<p>In accordance with data protection laws and regulations, you must ensure that any personal data you handle as part of your job responsibilities is processed lawfully, fairly, and transparently. You</p>

<!-- ═══════════════════════════════════════════ PAGE 3 ═══ -->
<div class="pb"></div>

<p>&nbsp;</p>
<p>must only collect and use personal data for legitimate business purposes and ensure that it is kept secure at all times. Any breach of confidentiality or data protection policies will be treated as a serious disciplinary matter and may result in termination of employment and legal action.</p>

<div class="h-teal">Declaration</div>

<p>I have read and accept all the terms and conditions of this offer and the enclosed annexure. I confirm that I am not entitled to any other benefits unless specifically agreed in writing by the company.</p>

<p><strong>Best Regards,</strong></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>{d.get('name','')}</p>
<p>{d.get('designation','')}</p>
<p>{d.get('location','Hyderabad')}</p>

<!-- ═══════════════════════════════════════════ PAGE 4 ═══ -->
<div class="pb"></div>

<p class="ann-title">Annexure</p>

<!-- Employee info -->
<table class="info-tbl">
  <tr><td class="lbl">Employee Name</td><td>{d.get('name','')}</td></tr>
  <tr><td class="lbl">Employee Id</td><td>{d.get('employee_id','')}</td></tr>
  <tr><td class="lbl">Designation</td><td>{d.get('designation','')}</td></tr>
  <tr><td class="lbl">Department</td><td>{d.get('department','Sales &amp; Marketing')}</td></tr>
</table>

<p class="ann-sub">Annexure I</p>

<!-- Salary table -->
<table class="sal-tbl">
  <tr class="hdr">
    <td>Salary Components</td>
    <td class="r">Per Month</td>
    <td class="r">Per Annum</td>
  </tr>
  <tr><td>Basic</td>             <td class="r">{self._fmt(m['basic'])}</td>   <td class="r">{self._fmt(a['basic'])}</td></tr>
  <tr><td>HRA</td>               <td class="r">{self._fmt(m['hra'])}</td>     <td class="r">{self._fmt(a['hra'])}</td></tr>
  <tr><td>LTA</td>               <td class="r">{self._fmt(m['lta'])}</td>     <td class="r">{self._fmt(a['lta'])}</td></tr>
  <tr><td>Other Allowance</td>   <td class="r">{self._fmt(m['other'])}</td>   <td class="r">{self._fmt(a['other'])}</td></tr>
  <tr class="bld"><td>Gross</td> <td class="r">{self._fmt(m['gross'])}</td>   <td class="r">{self._fmt(a['gross'])}</td></tr>
  <tr class="bld"><td>Employer Contributions</td><td></td><td></td></tr>
  <tr><td>Employer PF</td>       <td class="r">0</td>                         <td class="r">0</td></tr>
  <tr class="bld"><td>Total (A)</td><td class="r">0</td>                      <td class="r">0</td></tr>
  <tr class="hl"><td>CTC (Cost to company)</td><td class="r">{self._fmt(m['ctc'])}</td><td class="r">{self._fmt(a['ctc'])}</td></tr>
  <tr><td>Employee PF</td>        <td class="r">0</td>                        <td class="r">0</td></tr>
  <tr><td>Professional tax</td>   <td class="r">{self._fmt(m['pt'])}</td>     <td class="r">{self._fmt(a['pt'])}</td></tr>
  <tr class="bld"><td>Total(B)</td><td class="r">{self._fmt(m['total_b'])}</td><td class="r">{self._fmt(a['total_b'])}</td></tr>
  <tr class="bld"><td>Total Deductions(A+B)</td><td class="r">{self._fmt(m['deductions'])}</td><td class="r">{self._fmt(a['deductions'])}</td></tr>
  <tr class="hl"><td>Net Amount</td><td class="r">{self._fmt(m['net'])}</td>   <td class="r">{self._fmt(a['net'])}</td></tr>
</table>

<p><strong>({d.get('annual_ctc_words','')})</strong></p>
<p class="note-text"><strong>Note:</strong> Payment of perquisites, allowances, and reimbursements is subject to Income Tax provisions and company policies.</p>

<!-- Signatures -->
<div class="sig-block">
  <div class="sig-grid">
    <div class="sig-l">
      {sig_ceo}
      <strong>{d.get('ceo_name','Sanjay Kumar')}</strong><br>
      CEO<br>
      Email: Sanjay.kumar@petabytz.com
    </div>
    <div class="sig-r">
      <strong>Employee Signature:</strong>
    </div>
  </div>
</div>

</body>
</html>"""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_offer_letter(self, data: dict) -> str:
        """Generate PDF and return filepath."""
        ctc = float(data.get("annual_ctc", 0))
        if not data.get("annual_ctc_words"):
            data["annual_ctc_words"] = self._number_to_words(int(ctc))

        html = self._html(data)
        name = data.get("name", "Candidate").replace(" ", "_")
        filepath = os.path.join(self.output_dir, f"{name}_PetaBytz_Offer_Letter.pdf")

        HTML(string=html, base_url=self.base_dir).write_pdf(filepath)
        return filepath


# ── Standalone test ───────────────────────────────────────────────────
if __name__ == "__main__":
    gen = PetaBytzOfferLetterGenerator(output_dir="output")

    sample = {
        "date":             "28-October-2025",
        "name":             "Gampa Usha",
        "contact":          "8008809895",
        "location":         "Hyderabad, Telangana",
        "designation":      "Business Development Executive- IT Sales",
        "joining_date":     "Wednesday, 06th October 2025",
        "annual_ctc":       240000,
        "employee_id":      "PBTHYD0302",
        "department":       "Sales & Marketing",
        "work_shift":       "09:00 AM to 06:00 PM",
        "probation_period": "three months",
        "notice_period":    "two months",
        "ceo_name":         "Sanjay Kumar",
    }

    path = gen.generate_offer_letter(sample)
    print(f"✅  PDF saved: {path}")

    # Quick page-count check
    import fitz
    doc = fitz.open(path)
    print(f"    Pages: {len(doc)}")
    for i, pg in enumerate(doc):
        lines = [ln.strip() for ln in pg.get_text().splitlines() if ln.strip()]
        print(f"    Page {i+1} first line: {lines[0] if lines else '(empty)'}")
