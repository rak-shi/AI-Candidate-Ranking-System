import re

def clean_text(text):

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()