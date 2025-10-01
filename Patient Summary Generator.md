# Patient Summary Generator

``` Python

def generate_summary(record: dict) -> str:
    def g(keys, default):
        for k in keys:
            v = record.get(k)
            if v not in (None, ""):
                return v
        return default

    pid = g(("patient_id", "patientId", "id", "mrn"), "Unknown")
    age = g(("age", "Age", "years"), "?")
    gender = g(("gender", "Gender", "sex"), "?")

    diag = g(("diagnosis", "Diagnosis", "dx", "condition", "primary_dx"), None)
    if diag is None:
        ds = record.get("diagnoses")
        diag = "; ".join(map(str, ds)) if isinstance(ds, (list, tuple)) and ds else "Not specified"

    return f"Patient {pid}: {age}y, {gender}, Diagnosis = {diag}"

if __name__ == "__main__":
    sample = {"patientId": "P001", "Age": 30, "sex": "M", "diagnoses": ["Asthma", "Hypertension"]}
    print(generate_summary(sample))




