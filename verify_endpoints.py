import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_preview(company):
    print(f"Testing /preview for {company}...")
    payload = {
        'company_template': company,
        'candidate_name': 'Test Candidate Name',
        'pbt_candidate_name': 'Test Candidate Name PBT',
        'sss_candidate_name': 'Test Candidate Name SSS',
    }
    r = requests.post(f"{BASE_URL}/preview", data=payload)
    assert r.status_code == 200, f"Preview failed with status {r.status_code}"
    
    html = r.text
    if company == 'bluebix':
        assert 'BLUEBIX' in html or 'bluebix_offer.css' in html
    elif company == 'petabytz':
        assert 'PetaBytz' in html or 'petabytz_offer.css' in html
    elif company == 'softstandard':
        assert 'SOFTSTANDARD' in html or 'softstandard_offer.css' in html
    print(f"[OK] /preview for {company} passed.")

def test_generate(company):
    print(f"Testing /generate for {company}...")
    payload = {
        'company_template': company,
        'candidate_name': 'Test Candidate Name',
        'pbt_candidate_name': 'Test Candidate Name PBT',
        'sss_candidate_name': 'Test Candidate Name SSS',
    }
    r = requests.post(f"{BASE_URL}/generate", data=payload)
    assert r.status_code == 200, f"Generate failed with status {r.status_code}"
    assert r.content.startswith(b"%PDF-"), "Generated file is not a valid PDF"
    print(f"[OK] /generate for {company} passed (Valid PDF received).")

def test_email(company):
    print(f"Testing /email for {company}...")
    payload = {
        'company_template': company,
        'email': 'test@example.com',
        'candidate_name': 'Test Candidate Name',
        'pbt_candidate_name': 'Test Candidate Name PBT',
        'sss_candidate_name': 'Test Candidate Name SSS',
    }
    r = requests.post(f"{BASE_URL}/email", data=payload)
    assert r.status_code == 200, f"Email failed with status {r.status_code}"
    res = r.json()
    assert res['status'] == 'success', f"Unexpected status: {res}"
    assert 'successfully emailed' in res['message']
    print(f"[OK] /email for {company} passed.")

if __name__ == "__main__":
    try:
        for company in ['bluebix', 'petabytz', 'softstandard']:
            test_preview(company)
            test_generate(company)
            test_email(company)
        print("\nAll integration checks passed successfully!")
    except AssertionError as e:
        print(f"\nAssertion Error: {e}")
    except Exception as e:
        print(f"\nGeneral Error: {e}")
