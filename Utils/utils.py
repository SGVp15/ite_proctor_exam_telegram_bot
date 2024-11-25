import hashlib
import re


def to_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()


def clean_string(s: str) -> str:
    if type(s) is str:
        s = s.replace(',', ', ')
        s = re.sub(r'\s{2,}', ' ', s)
        s = s.strip()
    elif s in ('None', '#N/A', None):
        s = ''
    return s
