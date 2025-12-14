from fastapi import FastAPI
from .cache import semantic_lookup, store_cache
from .memory import save, load
from .agent import plan, execute, answer

app = FastAPI(title="Agentic Policy RAG")

@app.post("/query")
async def query(question: str, session_id: str = "default"):
    cached = semantic_lookup(question)
    if cached:
        print("Cache hit!")
        return {"answer": cached}

    memory = load(session_id)
    plan_json = plan(question, memory)
    context = execute(plan_json)
    final = answer(question, context, memory)

    store_cache(question, final)
    save(session_id, "user", question)
    save(session_id, "assistant", final)

    return {"answer": final}
