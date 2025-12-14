from pypdf import PdfReader

def load_pdf(path: str):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "page": i + 1,
                "text": text
            })

    return pages

def load_text(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [{"page": 1, "text": f.read()}]
