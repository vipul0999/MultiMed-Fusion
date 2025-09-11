# Medical Data Redaction and Validation

## Python Code

import re

def redact(text):
    patterns = {
        'name': r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",
        'phone': r"\(\d{3}\) \d{3}-\d{4}",
        'email': r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    }
    for key, pattern in patterns.items():
        text = re.sub(pattern, "[MASKED]", text)
    return text

def validate(data):
    if not all(k in data for k in ['name', 'record']):
        raise ValueError("Missing 'name' or 'record'")
    if not data['name'] or not data['record']:
        raise ValueError("Empty 'name' or 'record'")
    if not re.match(r"\d{4}-\d{2}-\d{2}", data.get('visit_date', '')):
        raise ValueError("Invalid 'visit_date' format")
    return True

data = {
    'name': 'Charan Reddy',
    'record': 'Patient has high blood pressure.',
    'visit_date': '2025-09-10'
}

redacted = redact(data['record'])

try:
    if validate(data):
        print(f"Validated: {redacted}")
except ValueError as e:
    print(f"Error: {e}")
    
    
