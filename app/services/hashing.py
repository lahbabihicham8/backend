import hashlib

def hash_sha256(value: str) -> str:
    if not value:
        return ""
    return hashlib.sha256(value.strip().lower().encode('utf-8')).hexdigest()
