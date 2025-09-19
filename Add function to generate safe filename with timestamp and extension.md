# Add function to generate safe filename with timestamp and extension

```Python
import re
from datetime import datetime

def make_safe_filename(text: str) -> str:
    text = text.strip().lower()
    safe = re.sub(r"[^a-z0-9-_]+", "_", text)
    return safe.strip("_")

def make_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def make_safe_file_with_timestamp(text: str, extension: str = "txt") -> str:
    """Generate a safe filename with a timestamp and given extension."""
    safe_name = make_safe_filename(text)
    ts = make_timestamp()
    return f"{safe_name}_{ts}.{extension}"

if __name__ == "__main__":
    sample_name = "Mohit Sai #123 (MRN: ABC-9999)"
    print(make_safe_filename(sample_name))   # original safe filename
    print(make_timestamp())                  # just timestamp
    print(make_safe_file_with_timestamp(sample_name, "pdf"))  # safe file with timestamp
