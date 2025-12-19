import hashlib
import os
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


def get_all_files_from_pattern(folder_input: str, pattern: str):
    file_list = []
    for root, dirs, files in os.walk(folder_input):
        for name in files:
            if name.endswith(pattern):
                file_list.append(os.path.join(root, name))
    return file_list
