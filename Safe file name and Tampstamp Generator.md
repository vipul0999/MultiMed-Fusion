# Safe file name and Tampstamp Generator

```Python
import re
from datetime import datetime

def make_safe_filename(text: str) -> str:
    text = text.strip().lower()
    safe = re.sub(r"[^a-z0-9-_]+", "_", text)
    return safe.strip("_")

def make_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if __name__ == "__main__":
    sample_name = "Mohit Sai #123 (MRN: ABC-9999)"
    print(make_safe_filename(sample_name))
    print(make_timestamp())
