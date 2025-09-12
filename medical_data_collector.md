# medical_data_collector.py
Collects lab results, prescriptions, and doctor notes into one patient record.

```
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

if __name__ == "__main__":
    # Example patient data
    lab_results = {"blood_pressure": "140/90", "cholesterol": "210 mg/dL"}
    prescriptions = ["Atorvastatin 10mg", "Lisinopril 20mg"]
    notes = "Patient complains of frequent headaches and dizziness."

    record = collect_patient_data(
        patient_id="P001",
        lab_results=lab_results,
        prescriptions=prescriptions,
        notes=notes
    )

    print("Collected Patient Record:")
    for key, value in record.items():
        print(f"{key}: {value}")
```
