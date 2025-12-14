import redis, numpy as np
from sentence_transformers import SentenceTransformer
from redis.commands.search.query import Query

from dotenv import load_dotenv
import os

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_THRESHOLD = float(os.getenv("CACHE_THRESHOLD", 0.4))
CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))  #

embedder = SentenceTransformer("all-MiniLM-L6-v2")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=False
)

def semantic_lookup(question):
    vector = np.array(embedder.encode(question), dtype=np.float32).tobytes()

    q = (
        Query("*=>[KNN 1 @embedding $vec AS score]")
        .return_fields("answer", "score")
        .dialect(2)
    )

    results = redis_client.ft("semantic_cache_index").search(
        q,
        query_params={"vec": vector}
    )

    if results.docs:
        score = float(results.docs[0].score)
        if score < CACHE_THRESHOLD:
            return results.docs[0].answer

    return None


def store_cache(question, answer):

    if not isinstance(answer, str):
        answer = str(answer)

    vector = np.array(embedder.encode(question), dtype=np.float32).tobytes()
    key = f"scache:{hash(question)}"

    redis_client.hset(
        key,
        mapping={
            "embedding": vector,
            "answer": answer
        }
    )
    redis_client.expire(key, CACHE_TTL)

