import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page \d+", "", text)
    return text.strip()
