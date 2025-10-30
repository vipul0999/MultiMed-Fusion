"""
data_audit_logger.py
Logs important system actions such as file uploads, summaries, and deletions
for compliance and traceability in MultiMed-Fusion.
"""

import json
from datetime import datetime
import os

LOG_FILE = "audit_log.json"

def log_event(event_type, user, description):
    """Record a system event in the audit log."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "user": user,
        "description": description
    }

    # Load existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    # Save back to file
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"[LOGGED] {event_type}: {description}")

if __name__ == "__main__":
    log_event("UPLOAD", "Dr. Vipul", "Uploaded new patient record P001.")
    log_event("SUMMARY_GENERATED", "System", "AI summary created for record P001.")
    log_event("DELETE", "Admin", "Removed expired patient file P001.")
