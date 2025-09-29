# Patient Summary Generator

``` Python

def generate_summary(record: dict) -> str:
    """
    Return a one-line summary from a patient record dict.
    Example fields expected: patient_id, age, gender, diagnosis
    """
    pid = record.get("patient_id", "Unknown")
    age = record.get("age", "?")
    gender = record.get("gender", "?")
    diag = record.get("diagnosis", "Not specified")
    return f"Patient {pid}: {age}y, {gender}, Diagnosis = {diag}"

if __name__ == "__main__":
    sample = {"patient_id": "P001", "age": 45, "gender": "M", "diagnosis": "Asthma"}
    print(generate_summary(sample))
