# Patient Data Summary Demo


```Python
from datetime import datetime, timezone
from statistics import mean

ISO = "%Y-%m-%dT%H:%M:%SZ"
parse = lambda s: datetime.strptime(s, ISO).replace(tzinfo=timezone.utc)
iso = lambda dt: dt.astimezone(timezone.utc).strftime(ISO)

def demo_data():
    return {
        "patient_id": "P569",
        "records": [
            {"type": "vitals", "timestamp": "2025-10-26T10:00:00Z", "bp": "120/80", "hr": 72},
            {"type": "lab", "timestamp": "2025-10-27T09:00:00Z", "glucose": 94},
            {"type": "lab", "timestamp": "2025-10-27T11:00:00Z", "glucose": 106},
            {"type": "note", "timestamp": "2025-10-27T12:30:00Z", "text": "Patient stable."}
        ]
    }

def glucose_stats(records):
    g = [r["glucose"] for r in records if r.get("type") == "lab" and "glucose" in r]
    if not g: return None
    return {"min": min(g), "max": max(g), "avg": round(mean(g), 1)}

def summarize(data):
    recs = data["records"]
    print("Patient:", data["patient_id"])
    print("Total records:", len(recs))
    print("Types:", {r["type"] for r in recs})
    g = glucose_stats(recs)
    if g: print(f"Glucose → min:{g['min']} max:{g['max']} avg:{g['avg']}")
    v = next((r for r in recs if r["type"] == "vitals"), None)
    if v: print(f"Latest vitals: BP {v['bp']}, HR {v['hr']}")

if __name__ == "__main__":
    summarize(demo_data())
