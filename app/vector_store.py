from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os   

load_dotenv()
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION = os.getenv("QDRANT_COLLECTION")

embedder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def search_internal(query, k=3):
    vector = embedder.encode(query).tolist()
    hits = qdrant.query_points(collection_name=COLLECTION, query=vector, limit=k).points

    return [
        f"[INTERNAL POLICY | {h.payload['department']} | {h.payload['doc_id']} {h.payload['version']} | page {h.payload['page']}]\n{h.payload['text']}"
        for h in hits
    ]
