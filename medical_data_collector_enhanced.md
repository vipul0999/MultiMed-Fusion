# 🩺 Medical Data Collector – JSON Export

This script is part of the **MultiMed Fusion** project.  
It collects patient medical data — such as **lab results, prescriptions, and doctor notes** — and saves them into a **structured JSON record**.  
The file can later be used for database ingestion, AI summarization, or system integration.

---

## 🧠 Overview

**Script Name:** `medical_data_collector_enhanced.py`  
**Purpose:** Collect, validate, and store patient medical data in a structured format.  
**Output Format:** JSON (`.json` file)  

---

## ⚙️ Features

- Combines multiple types of medical data into one structured record.  
- Automatically adds timestamps for traceability.  
- Validates input fields to prevent incomplete data.  
- Saves the collected data as a JSON file for future use.  
- Easily extendable for integration with MongoDB or APIs.  

---

## 🧩 Example Code

```python
import json
from datetime import datetime

def collect_patient_data(patient_id, lab_results, prescriptions, notes):
    """Combine different medical data sources into one structured record."""
    record = {
        "patient_id": patient_id,
        "visit_date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lab_results": lab_results,
        "prescriptions": prescriptions,
        "doctor_notes": notes
    }
    return record


def save_to_json(record, filename):
    """Save patient record to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(record, f, indent=4)
        print(f"✅ Record saved successfully to {filename}")
    except Exception as e:
        print(f"❌ Error saving record: {e}")


if __name__ == "__main__":
    # Example patient data
    lab_results = {
        "blood_pressure": "130/85 mmHg",
        "cholesterol": "190 mg/dL",
        "blood_sugar": "95 mg/dL"
    }
    prescriptions = ["Atorvastatin 10mg", "Lisinopril 20mg"]
    notes = "Patient reports mild fatigue and requests medication adjustment."

    # Create record
    record = collect_patient_data("P001", lab_results, prescriptions, notes)

    print("🩺 Collected Patient Record:")
    for key, value in record.items():
        print(f"{key}: {value}")

    # Save record as JSON
    save_to_json(record, "P001_record.json")


