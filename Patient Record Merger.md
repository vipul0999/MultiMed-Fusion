## Patient Record Merger

``` Python
import json
import os

def merge_patient_records(files, output_file):
    records = []
    for file in files:
        if os.path.exists(file):
            with open(file, "r") as f:
                records.append(json.load(f))
        else:
            print(f"Skipping missing file: {file}")

    with open(output_file, "w") as f:
        json.dump(records, f, indent=4)

    print(f"Merged {len(records)} records into {output_file}")

if __name__ == "__main__":
    patient_files = ["P001_record.json", "P002_record.json"]
    merge_patient_records(patient_files, "all_patient_records.json")
