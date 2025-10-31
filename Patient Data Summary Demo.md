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
            {"type": "lab",    "timestamp": "2025-10-27T09:00:00Z", "glucose": 94},
            {"type": "lab",    "timestamp": "2025-10-27T11:00:00Z", "glucose": 106},
            {"type": "note",   "timestamp": "2025-10-27T12:30:00Z", "text": "Patient stable."}
        ]
    }

def glucose_stats(records):
    g = [r["glucose"] for r in records if r.get("type") == "lab" and "glucose" in r]
    if not g: return None
    return {"min": min(g), "max": max(g), "avg": round(mean(g), 1), "n": len(g)}

def type_counts(records):
    c = {}
    for r in records: c[r["type"]] = c.get(r["type"], 0) + 1
    return c

# NEW: latest note text (visible output change)
def latest_note(records):
    notes = [r for r in records if r["type"] == "note"]
    return max(notes, key=lambda r: r["timestamp"])["text"] if notes else "none"

# NEW: quick status badge from glucose range (visible output change)
def status_badge(records):
    g = glucose_stats(records)
    if not g: return "status: no labs"
    return "status: ⚠ high glucose" if g["max"] >= 125 else "status: ok"

# NEW: recency signal (visible output change)
def days_since_last(records, now=None):
    now = now or datetime.now(timezone.utc)
    last = max(parse(r["timestamp"]) for r in records)
    return (now - last).days

def summarize(data):
    recs = data["records"]
    start = min(parse(r["timestamp"]) for r in recs)
    end   = max(parse(r["timestamp"]) for r in recs)
    now   = datetime.now(timezone.utc)
    print("Patient:", data["patient_id"])
    print("Now:", iso(now))
    print("Span:", iso(start), "→", iso(end), f"(+{days_since_last(recs, now)}d since last)")
    print("Type counts:", type_counts(recs))
    print("Latest note:", latest_note(recs))
    print(status_badge(recs))
    g = glucose_stats(recs)
    if g: print(f"Glucose → min:{g['min']} max:{g['max']} avg:{g['avg']} n:{g['n']}")

if __name__ == "__main__":
    summarize(demo_data())
