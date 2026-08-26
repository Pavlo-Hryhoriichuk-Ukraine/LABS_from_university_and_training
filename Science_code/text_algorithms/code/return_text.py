from pathlib import Path
from string import punctuation

def clean_text(text: str) -> str:
    CUSTOM_PUNCTUATION = punctuation + "«»—–’‘”“" + "1234567890"
    DELETE_TABLE = str.maketrans('', '', CUSTOM_PUNCTUATION)
    return text.strip().casefold().translate(DELETE_TABLE)