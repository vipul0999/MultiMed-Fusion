# Automated AI Summary Audit Logging System

This script automatically tracks key events such as **AI summary generation** and **Git commit actions**, ensuring transparency, traceability, and compliance in the MultiMed-Fusion system.

---

## Code

```python
import json
from datetime import datetime
from pathlib import Path

# Path to the audit log
AUDIT_LOG_PATH = Path("data/summary_audit_log.json")

# Function to log events (summary and commit events)
def log_event(event_type: str, **event_data):
    """Logs events related to AI summaries or commits."""
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    event_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    event_data["event_type"] = event_type

    # Read existing data
    data = []
    if AUDIT_LOG_PATH.exists():
        with open(AUDIT_LOG_PATH, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass

    # Append new event
    data.append(event_data)
    
    # Write updated data back to file
    with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"[INFO] {event_type.capitalize()} log updated for {event_data.get('commit_id', event_data.get('summary_id'))} by {event_data.get('user_name', event_data.get('doctor_id'))}")

# Function to get audit logs based on a specific field and value
def get_audit_logs(field: str, value: str):
    """Retrieves all audit logs filtered by a field and value."""
    if not AUDIT_LOG_PATH.exists():
        return []

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return []

    return [event for event in data if event.get(field) == value]

# Main driver
if __name__ == "__main__":
    # Log summary and commit events
    log_event("summary", summary_id="SUM123", patient_id="PAT456", doctor_id="DOC789", action="summary_generated")
    log_event("commit", commit_id="COMMIT123", user_name="Charan Reddy", commit_message="Implemented audit logging system")

    # Retrieve and print logs for patient and commit
    logs = get_audit_logs("patient_id", "PAT456")
    print(f"[INFO] Retrieved {len(logs)} logs.")
    
    commit_logs = get_audit_logs("user_name", "Charan Reddy")
    print(f"[INFO] Retrieved {len(commit_logs)} commit logs.")
