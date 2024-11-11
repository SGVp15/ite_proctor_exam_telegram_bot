import hashlib


def to_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()
