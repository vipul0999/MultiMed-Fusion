"""
Medical Data Collector with JSON Export (Enhanced Version)

This script collects patient information — including lab results, prescriptions,
and doctor notes — into a structured record and safely exports it to a JSON file.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def collect_patient_data(patient_id: str, lab_results: Dict[str, Any], prescriptions: List[str], notes: str) -> Dict[str, Any]:
    """
    Combine different medical data sources into one structured record.

    Args:
        patient_id (str): Unique identifier for the patient.
        lab_results (dict): Dictionary of lab test names and results.
        prescriptions (list): List of prescribed medications.
        notes (str): Doctor’s notes and observations.

    Returns:
        dict: A structured dictionary containing all patient data.
    """
    if not patient_id:
        raise ValueError("Patient ID cannot be empty.")
    if not isinstance(lab_results, dict) or not isinstance(prescriptions, list):
        raise TypeError("Lab results must be a dictionary and prescriptions must be a list.")

    record = {
        "patient_id": patient_id,
        "visit_date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lab_results": lab_results,
        "prescriptions": prescriptions,
        "doctor_notes": notes.strip()
    }

    return record


def save_to_json(record: Dict[str, Any], filename: str) -> None:
    """
    Save patient record to a JSON file with proper error handling.

    Args:
        record (dict): Patient data record.
        filename (str): File path for saving the record.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=4, ensure_ascii=False)
        print(f"✅ Record successfully saved to {filename}")
    except (OSError, TypeError) as e:
        print(f"❌ Error saving file {filename}: {e}")


def display_record_summary(record: Dict[str, Any]) -> None:
    """Display a readable summary of the collected patient record."""
    print("\n🩺 Patient Record Summary")
    print("-" * 40)
    for key, value in record.items():
        print(f"{key.capitalize()}: {value}")
    print("-" * 40)


if __name__ == "__main__":
    # Example patient data
    lab_results = {
        "blood_pressure": "140/90 mmHg",
        "cholesterol": "210 mg/dL",
        "blood_sugar": "108 mg/dL"
    }
    prescriptions = ["Atorvastatin 10mg", "Lisinopril 20mg"]
    notes = "Patient complains of frequent headaches and mild dizziness. Follow-up in 2 weeks."

    try:
        record = collect_patient_data("P001", lab_results, prescriptions, notes)
        display_record_summary(record)
        save_to_json(record, "P001_record.json")
    except Exception as e:
        print(f"⚠️ Error: {e}")
