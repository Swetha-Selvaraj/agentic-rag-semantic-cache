from .cache import redis_client

def save(session, role, text):
    redis_client.rpush(f"memory:{session}", f"{role}: {text}")

def load(session, limit=6):
    msgs = redis_client.lrange(f"memory:{session}", -limit, -1)
    return "\n".join(m.decode() for m in msgs)
