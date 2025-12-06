# 🧩 File Name Generator Script

This script safely generates filenames by removing special characters, adding timestamps, and appending extensions.  
Useful for saving medical reports, AI summaries, or logs in a consistent format.

---

## 📜 Code

```python
# file_name_generator.py
"""
Utility script for generating safe, timestamped filenames.
Ensures all saved files (reports, summaries, logs, etc.)
are uniquely identifiable and free from unsafe characters.
"""

import re
from datetime import datetime
from typing import Optional


def make_safe_filename(text: str) -> str:
    """
    Convert a given text into a safe filename by:
    - Converting to lowercase
    - Replacing non-alphanumeric characters with underscores
    - Stripping extra underscores

    Args:
        text (str): The raw input filename.

    Returns:
        str: Sanitized filename safe for file systems.
    """
    if not text:
        raise ValueError("Filename text cannot be empty.")
    text = text.strip().lower()
    safe = re.sub(r"[^a-z0-9-_]+", "_", text)
    return safe.strip("_")


def make_timestamp(fmt: Optional[str] = "%Y-%m-%d_%H-%M-%S") -> str:
    """
    Generate a timestamp string in the given format.

    Args:
        fmt (str, optional): Custom datetime format. Defaults to "%Y-%m-%d_%H-%M-%S".

    Returns:
        str: Current timestamp string.
    """
    return datetime.now().strftime(fmt)


def make_safe_file_with_timestamp(text: str, extension: str = "txt") -> str:
    """
    Generate a safe filename that includes a timestamp and file extension.

    Args:
        text (str): Raw text or filename to sanitize.
        extension (str): File extension (default: 'txt').

    Returns:
        str: Safe filename in format '<name>_<timestamp>.<extension>'.
    """
    safe_name = make_safe_filename(text)
    ts = make_timestamp()
    ext = extension.lstrip(".")  # Ensure no duplicate dot in extension
    return f"{safe_name}_{ts}.{ext}"


if __name__ == "__main__":
    sample_name = "Mohit Sai #123 (MRN: ABC-9999)"

    print("🧩 Original Safe Filename:")
    print(make_safe_filename(sample_name))

    print("\n🕒 Timestamp:")
    print(make_timestamp())

    print("\n📄 Safe File with Timestamp:")
    print(make_safe_file_with_timestamp(sample_name, "pdf"))
