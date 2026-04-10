import hashlib

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def batch_hash_from_filenames(file_names: list[str]) -> str:
    # requirement: hash of all the file names in the database (here: the selected batch)
    # deterministic order
    joined = "||".join(sorted([n or "" for n in file_names]))
    return sha256_hex(joined)  # 64 chars