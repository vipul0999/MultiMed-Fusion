# medical_data_collector.py
# Collects lab results, prescriptions, and doctor notes into one unified patient record.

from datetime import datetime
from typing import Dict, List, Any


def collect_patient_data(patient_id: str, lab_results: Dict[str, Any], prescriptions: List[str], notes: str) -> Dict[str, Any]:
    """
    Combine different medical data sources into one structured patient record.

    Args:
        patient_id (str): Unique patient identifier.
        lab_results (dict): Dictionary containing lab test names and results.
        prescriptions (list): List of prescribed medicines.
        notes (str): Doctor’s observation notes.

    Returns:
        dict: A structured patient record containing all combined medical data.
    """
    record = {
        "patient_id": patient_id,
        "visit_date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lab_results": lab_results,
        "prescriptions": prescriptions,
        "doctor_notes": notes
    }
    return record


if __name__ == "__main__":
    # Example patient data
    lab_results = {
        "blood_pressure": "140/90 mmHg",
        "cholesterol": "210 mg/dL",
        "blood_sugar": "110 mg/dL"
    }

    prescriptions = ["Atorvastatin 10mg", "Lisinopril 20mg"]
    notes = "Patient reports frequent headaches and mild dizziness. Needs follow-up in two weeks."

    # Generate the patient record
    record = collect_patient_data(
        patient_id="P001",
        lab_results=lab_results,
        prescriptions=prescriptions,
        notes=notes
    )

    # Display the collected record
    print("🩺 Collected Patient Record:")
    for key, value in record.items():
        print(f"{key}: {value}")
