# PatientHub – Simple Unified Patient Record Organizer

```Python
from collections import defaultdict

class PatientHub:
    def __init__(self):
        self.records = defaultdict(list)

    def add_record(self, patient_id, source, kind, note):
        entry = {
            "source": source,
            "kind": kind,
            "note": note
        }
        self.records[patient_id].append(entry)

    def unified_view(self, patient_id):
        return self.records.get(patient_id, [])

    def summary(self, patient_id):
        items = self.records.get(patient_id, [])
        kinds = sorted({item["kind"] for item in items})
        sources = sorted({item["source"] for item in items})
        summary_data = {
            "total_items": len(items),
            "kinds": kinds,
            "sources": sources
        }
        return summary_data


if __name__ == "__main__":
    hub = PatientHub()

    hub.add_record("P001", "hospital_db", "lab_result", "Blood test report: basic panel")
    hub.add_record("P001", "shared_drive", "imaging", "CT scan stored in imaging folder")
    hub.add_record("P001", "email", "referral", "Referral letter from cardiology department")
    hub.add_record("P002", "hospital_db", "note", "Summary of initial consultation")

    print("Unified view for patient P001:")
    for item in hub.unified_view("P001"):
        print(f"  - [{item['kind']}] from {item['source']} -> {item['note']}")

    print("\nSummary for patient P001:")
    summary = hub.summary("P001")
    print(f"  Total items: {summary['total_items']}")
    print(f"  Categories: {', '.join(summary['kinds'])}")
    print(f"  Sources: {', '.join(summary['sources'])}")


