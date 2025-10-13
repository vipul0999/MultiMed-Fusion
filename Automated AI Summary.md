# Automated AI Summary Audit Logging System

## Code

```Python
import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path("data/summary_audit_log.json")

def log_summary_event(summary_id: str, patient_id: str, doctor_id: str, action: str = "summary_generated"):
    

    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    event = {
        "summary_id": summary_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "action": action,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Append or create log file
    if AUDIT_LOG_PATH.exists():
        with open(AUDIT_LOG_PATH, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []  # Handle corrupted or empty files
            data.append(event)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as file:
            json.dump([event], file, indent=4)

    print(f"[INFO] Audit log updated for summary {summary_id} at {event['timestamp']}")

# Example usage
if __name__ == "__main__":
    log_summary_event("SUM123", "PAT456", "DOC789")
