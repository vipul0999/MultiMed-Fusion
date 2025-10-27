# Patient Data Summary Demo


```Python
from datetime import datetime, timezone

def demo_data():
    return {
        "patient_id": "P456",
        "records": [
            {"type": "vitals", "timestamp": "2025-10-26T10:00:00Z", "bp": "120/80", "hr": 72},
            {"type": "lab",    "timestamp": "2025-10-27T09:00:00Z", "glucose": 98},
            {"type": "lab",    "timestamp": "2025-10-27T11:00:00Z", "glucose": 102},
            {"type": "note",   "timestamp": "2025-10-27T12:30:00Z", "text": "Patient stable."}
        ]
    }

ISO = "%Y-%m-%dT%H:%M:%SZ"
parse = lambda s: datetime.strptime(s, ISO).replace(tzinfo=timezone.utc)
iso = lambda dt: dt.astimezone(timezone.utc).strftime(ISO)

def summarize(data):
    recs = data.get("records", [])
    print(" Multi Med Fusion — Quick Summary")
    print("-" * 40)
    print(f"Patient ID     : {data.get('patient_id', 'N/A')}")
    print(f"Total Records  : {len(recs)}")

    # counts by type
    counts = {}
    for r in recs:
        t = r.get("type", "unknown")
        counts[t] = counts.get(t, 0) + 1

    print("\nBy Type:")
    for t, c in counts.items():
        print(f" - {t}: {c}")

    # latest timestamp
    times = [parse(r["timestamp"]) for r in recs if "timestamp" in r]
    if times:
        print(f"\nLatest Record  : {iso(max(times))}")

    # tiny vitals snapshot (if present)
    vitals = [r for r in recs if r.get("type") == "vitals"]
    if vitals:
        v = vitals[-1]
        bp = v.get("bp", "N/A"); hr = v.get("hr", "N/A")
        print(f"Latest Vitals  : BP {bp}, HR {hr}")

    print("-" * 40)
    print("Demo complete (no files needed)")

if __name__ == "__main__":
    summarize(demo_data())
