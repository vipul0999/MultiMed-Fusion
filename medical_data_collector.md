#     Medical Data Collector with JSON Export
This Script Collects Patient information(lab results, prescriptions, and doctor notes) into a structured record and saves it to a JSON file.


``` python
import json
from datetime import datetime

def collect_patient_data(patient_id, lab_results, prescriptions, notes):
    """Combine different medical data sources into one structured record."""
    record = {
        "patient_id": patient_id,
        "visit_date": datetime.now().strftime("%Y-%m-%d"),
        "lab_results": lab_results,
        "prescriptions": prescriptions,
        "doctor_notes": notes
    }
    return record

def save_to_json(record, filename):
    """Save patient record to a JSON file."""
    with open(filename, "w") as f:
        json.dump(record, f, indent=4)

if __name__ == "__main__":
    # Example patient data
    lab_results = {"blood_pressure": "140/90", "cholesterol": "210 mg/dL"}
    prescriptions = ["Atorvastatin 10mg", "Lisinopril 20mg"]
    notes = "Patient complains of frequent headaches and dizziness."

    record = collect_patient_data("P001", lab_results, prescriptions, notes)

    print("Collected Patient Record:", record)

    # Save the record to a JSON file
    save_to_json(record, "P001_record.json")
    print("Record saved to P001_record.json")

