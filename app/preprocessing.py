import re
import string

def clean_text(text: str) -> str:
    """
    Basic text cleaning: lowercase, collapse whitespace, remove punctuation.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text