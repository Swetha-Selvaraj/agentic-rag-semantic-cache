

def chunk_text(text, max_tokens=400, overlap=60):
    """
    Splits by paragraphs and sentences heuristically.
    """
    sentences = text.replace("\n", " ").split(". ")
    chunks = []
    current = []
    length = 0

    for s in sentences:
        tokens = len(s.split())
        if length + tokens > max_tokens:
            chunks.append(" ".join(current))
            current = current[-overlap:] if overlap else []
            length = sum(len(x.split()) for x in current)

        current.append(s)
        length += tokens

    if current:
        chunks.append(" ".join(current))

    return chunks

    