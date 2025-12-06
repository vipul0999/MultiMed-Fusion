# Medical Data Redaction and Validation

This script anonymizes sensitive information in medical records and validates the required fields before processing.

```python
import re

def redact(text):
    """
    Redacts sensitive information (names, phone numbers, and emails) 
    from the given text using regular expressions.

    Args:
        text (str): Input string possibly containing sensitive info.

    Returns:
        str: Text with sensitive data replaced by [MASKED].
    """
    # Define regex patterns for sensitive data
    patterns = {
        'name': r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",
        'phone': r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        'email': r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    }

    # Replace each pattern with [MASKED]
    for key, pattern in patterns.items():
        text = re.sub(pattern, "[MASKED]", text)

    return text


def validate(data):
    """
    Validates a patient data dictionary for required fields and formats.

    Args:
        data (dict): Patient record data containing name, record, and visit_date.

    Raises:
        ValueError: If required fields are missing, empty, or incorrectly formatted.

    Returns:
        bool: True if validation passes.
    """
    required_fields = ['name', 'record', 'visit_date']

    # Check presence of required keys
    if not all(k in data for k in required_fields):
        raise ValueError("Missing one or more required fields: 'name', 'record', 'visit_date'.")

    # Check for empty values
    for field in required_fields:
        if not data[field]:
            raise ValueError(f"Field '{field}' cannot be empty.")

    # Validate visit date format (YYYY-MM-DD)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", data['visit_date']):
        raise ValueError("Invalid 'visit_date' format. Expected YYYY-MM-DD.")

    return True


if __name__ == "__main__":
    # Example input data
    data = {
        'name': 'Charan Reddy',
        'record': 'Patient Charan Reddy has high blood pressure. Contact: (123) 456-7890, charan@example.com',
        'visit_date': '2025-09-10'
    }

    try:
        if validate(data):
            redacted_text = redact(data['record'])
            print(f"Validated record:\n{redacted_text}")
    except ValueError as e:
        print(f"Validation Error: {e}")

