from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance



from pdf_loader import load_pdf, load_text
from cleaner import clean_text
from chunker import chunk_text
from embeddings import embed
    


qdrant = QdrantClient("localhost", port=6333)

COLLECTION = "company_policies"

qdrant.create_collection(
   collection_name=COLLECTION,
   vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

def ingest_policy(pdf_path, department, doc_id, version):
    pages = load_text(pdf_path)
    points = []

    for page in pages:
        cleaned = clean_text(page["text"])
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            points.append({
                "id": str(uuid4()),
                "vector": embed(chunk),
                "payload": {
                    "text": chunk,
                    "source": "company_policy",
                    "department": department,
                    "doc_id": doc_id,
                    "version": version,
                    "trust_level": "high",
                    "page": page["page"]
                }
            })

    qdrant.upsert(collection_name=COLLECTION, points=points)
    print(f"Ingested {len(points)} chunks")


if __name__ == "__main__":
    ingest_policy(
        pdf_path="/Users/swetha/Semantic/password_policy_v1.txt",
        department="Security",
        doc_id="password_policy",
        version="v1"
    )
    
    
